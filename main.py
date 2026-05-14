from fastmcp import FastMCP
from pathlib import Path
from mcp_server.browser_engine import BrowserManager  
from mcp_server.tools import register_tools

mcp = FastMCP("Operator-Server")
WORKSPACE   = Path(__file__).parent / "workspace"
WORKSPACE.mkdir(exist_ok=True)

browser_manager = BrowserManager(WORKSPACE)
register_tools(mcp, browser_manager, WORKSPACE)

if __name__ == "__main__":
    mcp.run()

