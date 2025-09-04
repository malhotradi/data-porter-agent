from google.adk.agents import LlmAgent
from .config import *
from .sub_agents.assessment_agent.agent import mysql_assessor_agent
from .prompt import DATA_PORTER_PROMPT
# Define the root agent, which acts as a dispatcher
root_agent = LlmAgent(
    name='data_porter_agent',
    model=MODEL,
    instruction=DATA_PORTER_PROMPT,
    # Register the assessor as a sub-agent
    sub_agents=[mysql_assessor_agent],
)