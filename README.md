# atlassian-mcp

A read-only MCP server exposing Jira and Confluence operations to Claude.

> **Status:** Work in progress. This README is a placeholder; the production version (architecture diagram, demo, scope) replaces it before the repo is published.

## Quick start

1. Copy `.env.example` to `.env` and fill in your Atlassian email, API token, and tenant URL. Generate a token at <https://id.atlassian.com/manage-profile/security/api-tokens>.
2. Install dependencies:
   ```
   uv sync
   ```
   (or `pip install -e .` if you don't use uv)
3. Run the server on stdio (the transport Claude Desktop uses):
   ```
   uv run atlassian-mcp
   ```

## Available tools

- `list_open_tickets_by_component(project_key, component, limit=25)` — open issues in a project, filtered by component, sorted by priority then last-updated.

Planned (per the strategy doc):
- `summarise_recent_changes`
- `find_assets_referencing`
- `generate_weekly_status_from_jira`

## Adding a tool

Edit `src/atlassian_mcp/server.py`, add a function decorated with `@mcp.tool()`, and call into `AtlassianClient` (in `src/atlassian_mcp/atlassian.py`) for the REST work.

## Auth

Atlassian API token (basic auth: email + token). OAuth 2.0 / 3LO is intentionally out of scope for v1 — the production path, but adds a day for this artefact's purpose.

## What's not in scope

- Write operations (create/transition/delete issues). Read-only by design — keeps the demo safe to talk through at interview.
- Anything outside Jira and Confluence.
