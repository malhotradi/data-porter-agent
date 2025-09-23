# app/utils/common_tools.py
from google.adk.tools import FunctionTool
from google.cloud import storage
from io import BytesIO
import os
import tempfile
import markdown2
from xhtml2pdf import pisa
import logging

logger = logging.getLogger(__name__)


def save_report_as_pdf(report_markdown: str, filename: str = "assessment/final_assessment.pdf") -> str:
    """
    Receives a pre-formatted Markdown string, converts it directly to a PDF,
    uploads it to a GCS bucket, and returns a public URL for the file.
    """
    logger.info(f"Received final markdown report. Starting PDF conversion and upload to {filename}")
    
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    if not bucket_name:
        logger.error("GCS_BUCKET_NAME env variable not set.")
        return "Error: GCS_BUCKET_NAME is not configured in the environment."

    try:
        # Use a temporary file to handle the PDF creation
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            # 1. Convert the received Markdown string to HTML
            html = markdown2.markdown(report_markdown, extras=["tables", "fenced-code-blocks"])
            
            # 2. Create the PDF from the HTML
            pisa_status = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=tmp)
            
            if pisa_status.err:
                logger.error(f"PDF conversion failed: {pisa_status.err}")
                return f"Error converting to PDF: {pisa_status.err}"
            
            tmp_path = tmp.name

        # 3. Upload the created PDF file to GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_filename(tmp_path, content_type='application/pdf')
        
        # 4. Clean up the local temporary file
        os.remove(tmp_path)

        # 5. Return the public URL for the uploaded file
        public_url = f"https://storage.googleapis.com/{bucket_name}/{filename}"
        logger.info(f"Successfully uploaded report to {public_url}")
        
        return f"Successfully created and uploaded the report. It is accessible at: {public_url}"

    except Exception as e:
        logger.exception(f"An unexpected error occurred during PDF save: {e}")
        return f"An unexpected error occurred: {e}"

    
# --- EXPORT THE SIMPLIFIED TOOL FOR THE ROOT AGENT ---
# The root agent's prompt refers to a tool named 'save_report_tool'.
save_report_tool = FunctionTool(
    func=save_report_as_pdf
)