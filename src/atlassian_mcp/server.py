from mcp.server.fastmcp import FastMCP

from .atlassian import AtlassianClient

mcp = FastMCP("atlassian-mcp")
_client = AtlassianClient.from_env()


@mcp.tool()
async def list_open_tickets_by_component(
    project_key: str,
    component: str,
    limit: int = 25,
) -> list[dict]:
    """List open Jira tickets in a project filtered by component.

    Returns issues whose status category is not Done, sorted by priority
    then last-updated. Use this to triage what's currently in flight for
    a given component.
    """
    jql = (
        f'project = "{project_key}" '
        f'AND component = "{component}" '
        'AND statusCategory != Done '
        'ORDER BY priority DESC, updated DESC'
    )
    return await _client.search_jira(jql, limit=limit)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
