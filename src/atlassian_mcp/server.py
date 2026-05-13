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


@mcp.tool()
async def generate_weekly_status_from_jira(
    project_key: str,
    days: int = 7,
) -> dict:
    """Summarise tickets resolved in the last N days, grouped by component.

    Use this to draft a weekly status update. Returns the total resolved
    count and the list of closed tickets organised by component, treating
    component as the owning team. Tickets with no component fall under
    "(no component)".
    """
    issues = await _client.recently_resolved(project_key, days=days)

    by_component: dict[str, list[dict]] = {}
    for issue in issues:
        components = issue["components"] or ["(no component)"]
        for c in components:
            by_component.setdefault(c, []).append(
                {
                    "key": issue["key"],
                    "summary": issue["summary"],
                    "assignee": issue["assignee"],
                    "resolved": issue["resolved"],
                }
            )

    return {
        "project": project_key,
        "window_days": days,
        "total_resolved": len(issues),
        "by_component": by_component,
    }


def main() -> None:
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--list-tools":
        _list_tools()
        return
    mcp.run()


def _list_tools() -> None:
    import asyncio

    for t in asyncio.run(mcp.list_tools()):
        print(f"\n{t.name}")
        if t.description:
            print(f"  {t.description.strip().splitlines()[0]}")
        params = list((t.inputSchema or {}).get("properties", {}).keys())
        if params:
            print(f"  args: {', '.join(params)}")
    print()


if __name__ == "__main__":
    main()
