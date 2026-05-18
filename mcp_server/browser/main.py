from fastmcp import FastMCP

from mcp_server.browser.engine import BrowserManager
from mcp_server.browser.tools import register_tools

mcp = FastMCP("Browser-Server")

browser_manager = BrowserManager()
register_tools(mcp, browser_manager)

if __name__ == "__main__":
    mcp.run()
