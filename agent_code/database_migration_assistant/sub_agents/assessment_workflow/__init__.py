from google.adk.agents import SequentialAgent
from .raw_assessment_agent import worker_agent
from .structured_assessment_agent import formatter_agent
from .report_agent import pdf_agent

# This SequentialAgent defines the workflow: run the worker, then the formatter.
# The state (`raw_assessment_data`) is automatically passed between them.
assessment_workflow = SequentialAgent(
    name="assessment_workflow",
    sub_agents=[worker_agent, formatter_agent, pdf_agent]
)