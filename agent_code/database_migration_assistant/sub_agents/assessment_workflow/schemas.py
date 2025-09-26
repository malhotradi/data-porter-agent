# app/sub_agents/assessment/schemas.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Input Schema (No changes needed) ---
class AssessmentInput(BaseModel):
    """Defines the structured input required by the assessment agent."""
    db_type: str = Field(
        description="The specific database type (e.g., 'mysql', 'postgres', 'sqlserver') that the user wants to assess.")
    db_host: str = Field(
        description="The hostname or IP address of the customer's database server.")
    db_port: int = Field(
        description="The network port the database server is listening on.")
    db_user: str = Field(
        description="The username for connecting to the database.")
    db_password: str = Field(
        description="The password for the database user.")

# --- Granular Models for the Output Schema ---

class ServerConfig(BaseModel):
    """Contains details about the source database server configuration."""
    db_version: str = Field(description="The full version string of the database server.")
    operating_system: Optional[str] = Field(None, description="The operating system of the database server, if available.")

class DatabaseDetail(BaseModel):
    """Contains inventory details for a single database."""
    database_name: str
    size_mb: float = Field(description="The size of the database in megabytes.")
    default_character_set: str
    default_collation: str
    engine: Optional[str] = Field(None, description="The storage engine used by the tables in database (e.g., InnoDB, MyISAM).")

class ColumnDetail(BaseModel):
    """Describes a single column in a database table."""
    column_name: str
    data_type: str
    is_nullable: str

class TableDetail(BaseModel):
    """Describes a single table within a schema."""
    table_name: str
    row_count: int
    columns: List[ColumnDetail] = Field(description="A list of column names and their data types.")
    primary_key: List[str] = Field(description="A list of primary keys in table.")
    indexes: List[str] = Field(description="A list of indexes in the table.")

class ViewDetail(BaseModel):
    """Describes a single view and its dependencies."""
    view_name: str
    parent_tables: List[str] = Field(description="A list of tables this view depends on.")

class SchemaDetails(BaseModel):
    """Contains a detailed breakdown of all objects within a single schema."""
    tables: List[TableDetail]
    views: Optional[List[ViewDetail]] = Field(None, description="A list of view details.")
    stored_procedures: Optional[List[str]] = Field(None, description="A list of stored procedure names.")
    functions: Optional[List[str]] = Field(None, description="A list of function names.")
    triggers: Optional[List[str]] = Field(None, description="A list of trigger names.")

class Risk(BaseModel):
    """Describes a single identified migration risk."""
    level: str = Field(description="The severity of the risk (e.g., 'High', 'Medium', 'Low').")
    description: str = Field(description="A detailed description of the risk.")
    recommendation: str = Field(description="The recommended action to mitigate the risk.")

# --- Main Output Schema ---

class AssessmentReport(BaseModel):
    """Defines the structure of the detailed assessment report."""
    executive_summary: str = Field(
        description="A high-level overview of the findings and a final **Migration Complexity Score** (Low, Medium, High, Very High).")
    server_config: ServerConfig
    database_inventory: List[DatabaseDetail]
    schema_breakdown: Dict[str, SchemaDetails] = Field(
        description="A dictionary where keys are schema names, containing the detailed breakdown of their objects.")
    risks_and_recommendations: List[Risk]

class AssessmentOutput(BaseModel):
    """The final, complete structured output object that the assessment agent MUST return."""
    report: AssessmentReport = Field(
        description="The complete, detailed assessment report object containing all findings.")