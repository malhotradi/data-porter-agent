# tools.py

from toolbox_core import ToolboxSyncClient
import markdown2
import os
import tempfile
from xhtml2pdf import pisa
from io import BytesIO
from google.adk.tools import FunctionTool, ToolContext
from google.cloud import storage
from google.adk.artifacts import GcsArtifactService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create a single, shared client instance that connects to the toolbox server.
# The server is started by the `genai-toolbox` command.
toolbox_client = ToolboxSyncClient("http://127.0.0.1:5000")

# This file now only defines and exports the raw Python function.
def save_report_as_pdf(report_markdown: str, filename: str = "assessment/assessment_report.pdf") -> str:
    """
    Converts a Markdown string into a PDF, uploads it to a GCS bucket,
    and returns a public URL for the file.
    """
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    if not bucket_name:
        return "Error: GCS_BUCKET_NAME is not configured in the environment."

    try:
        # Use a temporary file to avoid cluttering the local disk
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            # 1. Convert Markdown to HTML
            html = markdown2.markdown(report_markdown, extras=["tables"])
            
            # 2. Create the PDF in the temporary file
            pisa_status = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=tmp)
            
            if pisa_status.err:
                return f"Error converting to PDF: {pisa_status.err}"
            
            tmp_path = tmp.name

        # 3. Upload the temporary file to GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_filename(tmp_path, content_type='application/pdf')
        
        # Clean up the temporary file
        os.remove(tmp_path)

        # 4. Return the public URL
        public_url = f"https://storage.googleapis.com/{bucket_name}/{filename}"
        
        return f"Successfully created and uploaded the report. It is accessible at: {public_url}"

    except Exception as e:
        return f"An unexpected error occurred: {e}"

async def list_artifacts_tool(tool_context: ToolContext) -> str:
    """Tool to list available artifacts for the user."""
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    #### Inject GcsArtifactService in tool_context
    gcs_service = GcsArtifactService(bucket_name="data-porter-agent")
    tool_context._invocation_context.artifact_service = gcs_service
    ####
    
    available_files = await tool_context.load_artifact(filename='assessment_report.pdf')
    logger.info(available_files)
    return available_files
save_report_as_pdf_tool = FunctionTool(func=save_report_as_pdf)
list_artifacts_tool = FunctionTool(func=list_artifacts_tool)

