# agent.py

from google.adk.agents import LlmAgent
from .tools import toolbox_client
from data_porter_agents.config import *
from data_porter_agents.prompt import MYSQL_ASSESSOR_PROMPT
from .tools import save_report_as_pdf_tool,list_artifacts_tool
# Define the assessor sub-agent

tool_list=[]
tool_list.extend(toolbox_client.load_toolset("assessment-toolset"))
tool_list.extend([save_report_as_pdf_tool])

mysql_assessor_agent = LlmAgent(
    name='mysql_assessor_agent',
    model=MODEL,
    instruction=MYSQL_ASSESSOR_PROMPT,
    # This agent only gets the tools it needs from the 'assessment-toolset'
    tools=tool_list
)