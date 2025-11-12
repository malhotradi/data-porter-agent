# app/utils/common_tools.py
from google.adk.tools import FunctionTool
from google.cloud import storage
from io import BytesIO
import os
import tempfile
from xhtml2pdf import pisa
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def _format_report_to_html(report_data: Dict[str, Any]) -> str:
    """
    Converts the structured JSON report data into a beautifully formatted HTML string.
    """
    # This is a detailed HTML template with CSS for a professional look.
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; margin: 2em; color: #333; }}
            h1, h2, h3, h4, h5 {{ color: #1a73e8; }}
            h1 {{ text-align: center; border-bottom: 2px solid #1a73e8; padding-bottom: 10px; }}
            h2 {{ border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-top: 2em; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 1.5em; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; word-wrap: break-word; }}
            th {{ background-color: #f2f8ff; font-weight: bold; }}
            .code {{ font-family: monospace; background-color: #eee; padding: 2px 4px; border-radius: 3px; }}
            .summary p {{ line-height: 1.6; }}
        </style>
    </head>
    <body>
        <h1>Database Migration Assessment Report</h1>
        
        <div class="summary">
            <h2>1. Executive Summary</h2>
            <p>{report_data.get('executive_summary', 'Not provided.')}</p>
        </div>
        
        <h2>2. Server Configuration</h2>
        <table>
            <tr><th>Parameter</th><th>Value</th></tr>
            <tr><td>DB Version</td><td>{report_data.get('server_config', {}).get('db_version', 'N/A')}</td></tr>
            <tr><td>Operating System</td><td>{report_data.get('server_config', {}).get('operating_system', 'N/A')}</td></tr>
        </table>

        <h2>3. Database Inventory</h2>
        <table>
            <tr><th>Database Name</th><th>Size (MB)</th><th>Default Engine</th><th>Default Character Set</th><th>Default Collation</th></tr>
    """
    for db in report_data.get('database_inventory', []):
        html += f"""
            <tr>
                <td>{db.get('database_name', 'N/A')}</td>
                <td>{db.get('size_mb', 'N/A')}</td>
                <td>{db.get('engine', 'N/A')}</td>
                <td>{db.get('default_character_set', 'N/A')}</td>
                <td>{db.get('default_collation', 'N/A')}</td>
            </tr>
        """
    html += "</table>"

    html += "<h2>4. Schema Breakdown</h2>"
    for schema_name, schema_details in report_data.get('schema_breakdown', {}).items():
        html += f"<h3>Schema: <span class='code'>{schema_name}</span></h3>"
        
        html += "<h4>4.1 Tables</h4>"
        for table in schema_details.get('tables', []):
            html += f"<h5>Table: <span class='code'>{table.get('table_name', 'N/A')}</span></h5>"
            html += f"<p><strong>Row Count:</strong> {table.get('row_count', 'N/A')}</p>"
            # This is the corrected section that renders the column details
            html += "<table><tr><th>Column Name</th><th>Data Type</th><th>Nullable</th></tr>"
            for col in table.get('columns', []):
                html += f"""
                    <tr>
                        <td><span class='code'>{col.get('column_name', 'N/A')}</span></td>
                        <td>{col.get('data_type', 'N/A')}</td>
                        <td>{col.get('is_nullable', 'N/A')}</td>
                    </tr>
                """
            html += "</table>"

        html += "<h4>4.2 Views</h4>"
        if not schema_details.get('views'):
            html += "<p>No views found.</p>"
        else:
            html += "<table><tr><th>View Name</th><th>Parent Tables</th></tr>"
            for view in schema_details.get('views', []):
                parent_tables_str = ", ".join(f"<span class='code'>{pt}</span>" for pt in view.get('parent_tables', []))
                html += f"""
                    <tr>
                        <td><span class='code'>{view.get('view_name', 'N/A')}</span></td>
                        <td>{parent_tables_str}</td>
                    </tr>
                """
            html += "</table>"
            
    html += "<h2>5. Risks and Recommendations</h2>"
    html += "<table><tr><th>Risk Level</th><th>Description</th><th>Recommendation</th></tr>"
    for risk in report_data.get('risks_and_recommendations', []):
        html += f"""
            <tr>
                <td>{risk.get('level', 'N/A')}</td>
                <td>{risk.get('description', 'N/A')}</td>
                <td>{risk.get('recommendation', 'N/A')}</td>
            </tr>
        """
    html += "</table>"
    
    html += "</body></html>"
    return html


def save_report_as_pdf(assessment_json: Dict[str, Any], filename: str = "assessment/final_assessment.pdf") -> str:
    """
    Receives a JSON object with assessment findings, converts it to a formatted
    HTML report, generates a PDF, uploads it to GCS, and returns a public URL.
    """
    logger.info("Received assessment JSON. Starting HTML conversion and PDF generation.")
    
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    if not bucket_name:
        logger.error("GCS_BUCKET_NAME env variable not set.")
        return "Error: GCS_BUCKET_NAME is not configured in the environment."

    try:
        html_content = _format_report_to_html(assessment_json.get('report', {}))
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pisa_status = pisa.CreatePDF(BytesIO(html_content.encode('UTF-8')), dest=tmp)
            
            if pisa_status.err:
                logger.error(f"PDF conversion failed: {pisa_status.err}")
                return f"Error converting to PDF: {pisa_status.err}"
            
            tmp_path = tmp.name

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_filename(tmp_path, content_type='application/pdf')
        
        os.remove(tmp_path)

        public_url = f"https://storage.googleapis.com/{bucket_name}/{filename}"
        logger.info(f"Successfully uploaded report to {public_url}")
        
        return f"Successfully created and uploaded the report. It is accessible at: {public_url}"

    except Exception as e:
        logger.exception(f"An unexpected error occurred during PDF save: {e}")
        return f"An unexpected error occurred: {e}"

    
save_report_tool = FunctionTool(func=save_report_as_pdf)