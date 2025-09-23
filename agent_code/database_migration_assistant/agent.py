# app/agent.py
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from .prompt import DATA_PORTER_PROMPT

# Import the TWO tools the Root Agent will use
from database_migration_assistant.sub_agents.assessment_agent import assessment_agent
from database_migration_assistant.utils.common_tools import save_report_tool

# --- 1. Initialization ---
load_dotenv()

# --- 3. Define the Root Agent ---
# This agent no longer has sub-agents. It orchestrates using tools.
root_agent = LlmAgent(
    name='data_porter_agent',
    model='gemini-2.5-pro',
    instruction=DATA_PORTER_PROMPT,
    sub_agents=[
        assessment_agent 
    ],
    tools=[
        save_report_tool 
    ]
)