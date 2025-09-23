
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import SseConnectionParams 

connection_params=SseConnectionParams(
        url="http://127.0.0.1:5000/mcp/sse", 
        headers={}
)

mcp_toolset = MCPToolset(connection_params = connection_params)
