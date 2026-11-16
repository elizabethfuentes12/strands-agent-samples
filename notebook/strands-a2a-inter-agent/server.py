# MCP Python SDK 2.x: FastMCP was renamed to MCPServer.
# Migration guide: https://py.sdk.modelcontextprotocol.io/v2/migration/
from mcp.server.mcpserver import MCPServer

from employee_data import SKILLS, EMPLOYEES

mcp = MCPServer("employee-server")

@mcp.tool()
def get_skills() -> set[str]:
    """all of the skills that employees may have - use this list to figure out related skills"""
    print("get_skills")
    return SKILLS

@mcp.tool()
def get_employees_with_skill(skill: str) -> list[dict]:
    """employees that have a specified skill - output includes fullname (First Last) and their skills"""
    print(f"get_employees_with_skill({skill})")
    skill_lower = skill.lower()
    employees_with_skill = [employee for employee in EMPLOYEES if any(s.lower() == skill_lower for s in employee["skills"])]
    if not employees_with_skill:
        raise ValueError(f"No employees have the {skill} skill")
    return employees_with_skill

if __name__ == "__main__":
    # In SDK 2.x transport options (host, port, stateless_http) are passed to run(), not the constructor.
    # Streamable HTTP endpoint: http://127.0.0.1:8002/mcp
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8002, stateless_http=True)
