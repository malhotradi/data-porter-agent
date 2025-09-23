from dotenv import load_dotenv
from google.adk.agents import Agent
from .tools import mcp_toolset
from .prompt import ASSESSOR_PROMPT
from .schemas import *
load_dotenv()

assessment_agent = Agent(
        model='gemini-2.5-pro',
        name='assessment_agent',
        description="Agent to output the assessment report of the given database type",
        instruction=ASSESSOR_PROMPT,
        tools=[mcp_toolset],
        input_schema=AssessmentInput,
        # output_schema=AssessmentOutput,
)