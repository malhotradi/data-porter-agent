# app/sub_agents/assessment/schemas.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class AssessmentInput(BaseModel):
    """
    Defines the structured input required by the assessment agent.
    """
    db_type: str = Field(
        description="The specific database type (e.g., 'mysql', 'postgres', 'sqlserver') that the user wants to assess.")
    db_host: str = Field(
        description="The hostname or IP address of the customer's database server.")
    db_port: int = Field(
        description="The network port the database server is listening on (e.g., 3306 for MySQL, 5432 for PostgreSQL).")
    db_user: str = Field(
        description="The username for connecting to the database.")
    db_password: str = Field(
        description="The password for the database user.")
    
class AssessmentReport(BaseModel):
    """
    Defines the structure of the detailed assessment report.
    This version is updated to match the actual JSON output from the sub-agent.
    """
    # FIX: The agent is producing a raw string for the summary.
    executive_summary: str = Field(
        description="A string containing the high-level summary.")
    
    # FIX: The agent is producing a dictionary for server config.
    server_config: Dict[str, Any] = Field(
        description="A dictionary of server configuration parameters.")
    
    # FIX: The agent is producing a dictionary for the inventory.
    database_inventory: Dict[str, Any] = Field(
        description="A dictionary containing lists of schemas.")
    
    # FIX: The agent is producing a dictionary for the breakdown.
    schema_breakdown: Dict[str, Any] = Field(
        description="A dictionary where keys are schema names, containing details of tables, views, etc.")
    
    # FIX: The agent is producing a dictionary for risks.
    risks_and_recommendations: Dict[str, Any] = Field(
        description="A dictionary containing lists of risks and recommendations.")

class AssessmentOutput(BaseModel):
    """
    The final, complete structured output object that the assessment agent MUST return.
    """
    report: AssessmentReport = Field(
        description="The complete, detailed assessment report object containing all findings.")
