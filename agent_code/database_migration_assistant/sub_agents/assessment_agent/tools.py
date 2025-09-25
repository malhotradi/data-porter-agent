
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import SseConnectionParams 

connection_params=SseConnectionParams(
        url="https://mcp-toolbox-1041111835370.us-central1.run.app/mcp/sse", 
        headers={}
)

mcp_toolset = MCPToolset(connection_params = connection_params)