from google.adk.agents import Agent
from .schemas import AssessmentOutput
from .prompt import FORMATTER_PROMPT

formatter_agent = Agent(
    name='formatter_agent',
    description="Formats raw text into the final AssessmentOutput JSON.",
    instruction=FORMATTER_PROMPT,
    # This enforces the final output structure
    output_schema=AssessmentOutput,
    # The validated JSON is then saved to a new state key.
    output_key="structured_assessment_report",
)