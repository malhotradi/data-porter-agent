from google.adk.agents import Agent
from ...utils.common_tools import save_report_tool
from .prompt import PDF_PROMPT

pdf_agent = Agent(
    name='pdf_agent',
    instruction=PDF_PROMPT,
    tools=[save_report_tool],
    # The final output of the entire workflow is the URL.
    output_key="final_report_url",
)