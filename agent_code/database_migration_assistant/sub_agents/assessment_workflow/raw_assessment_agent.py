from google.adk.agents import Agent
from .tools import mcp_toolset
from .schemas import AssessmentInput
from .prompt import WORKER_PROMPT

worker_agent = Agent(
    name='worker_agent',
    description="Uses MCP tools to gather raw database assessment data.",
    instruction=WORKER_PROMPT,
    tools=[mcp_toolset],
    input_schema=AssessmentInput,
    # This is key: it saves the raw text output to the session state
    output_key="raw_assessment_data",
)