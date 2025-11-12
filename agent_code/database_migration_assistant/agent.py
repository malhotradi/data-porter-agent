# app/agent.py
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from .prompt import DATA_PORTER_PROMPT
from database_migration_assistant.sub_agents.assessment_workflow import assessment_workflow

load_dotenv()

root_agent = Agent(
    name='data_porter_agent',
    model='gemini-2.5-pro',
    instruction=DATA_PORTER_PROMPT,
    sub_agents=[
        assessment_workflow
    ],
)