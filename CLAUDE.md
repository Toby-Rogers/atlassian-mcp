# CLAUDE.md

Briefing for any Claude Code session opened in this repo. Read this first.

---

## What this project is

A **read-only MCP server** that exposes a few Jira / Confluence operations to Claude as tools. It is being built primarily as a **portfolio artefact** — a credible piece of evidence on Toby Rogers' GitHub profile (`Toby-Rogers/atlassian-mcp`, eventually) for the Atlassian-track job pipeline.

It is also intended to be useful: once it works, Toby can use it on his own InvestCloud Jira tenant to triage tickets in plain English faster than the Jira UI.

## How this project came to exist

This was scaffolded across an earlier Claude Code session in a different workspace (`C:\Claude\Epic ME`), where the strategic framing was developed in `project/GitHub additions/demo-repo-strategy.md`. It was then relocated here so it can live as a standalone project. The strategy doc is the canonical "why" — read it if more context is needed.

### The original framing question (Toby, verbatim)

> 1. Atlassian MCP server (highest leverage — recommended)
> A read-only MCP server that exposes a few Jira/Confluence operations as Claude tools — e.g. `list_open_tickets_by_component`, `summarise_recent_changes`, `find_assets_referencing`. Thin wrapper over the official Atlassian REST API.
>
> How would I start on this project to add to my github. Can you guide me through the steps on what I have to do.

### The plain-English explanation of what an MCP server does (verbatim from the prior session)

> Fair question — I jumped into the build without explaining the point clearly. Let me back up.
>
> **What an MCP server actually is:** An MCP server is a small program that gives Claude new tools it didn't have before. Claude on its own doesn't know anything about your Jira instance. With this server running, Claude can call functions you've defined — and those functions hit Atlassian's REST API on Claude's behalf.
>
> So you go from this:
> > **Toby:** "What open tickets are in the BI component on the IC project?"
> > **Claude:** "I don't have access to your Jira. You'll need to check it manually."
>
> To this:
> > **Toby:** "What open tickets are in the BI component on the IC project?"
> > **Claude:** *(calls `list_open_tickets_by_component("IC", "BI")` against your Jira)* "There are 12 open tickets. Top priority: IC-4521 (P1, assigned to X, updated yesterday)…"
>
> Claude doesn't know SQL or JQL on your tenant. The MCP server is the bridge.

Re-read this if you ever lose sight of what is being built.

---

## Locked decisions (do not re-litigate without asking)

| Decision | Choice | Why |
|---|---|---|
| Language | **Python** (≥3.11) | Toby's choice 2026-05-08 |
| MCP SDK | **`mcp[cli]>=1.12,<2`** (FastMCP API) | Current official SDK |
| HTTP client | **httpx** (async) | Modern, plays nicely with FastMCP's async tools |
| Atlassian auth | **API token** (basic auth: email + token) | Faster than OAuth; appropriate for a demo. OAuth 3LO is explicitly **out of scope for v1** — call it out in the README as the production path |
| Scope | **Read-only** | No create/transition/delete. Senior signal at interview ("safe to talk through") |
| Transport | **stdio** (default) | Claude Desktop's transport |
| Repo name | `atlassian-mcp` | Avoids clash with the popular `sooperset/mcp-atlassian`. Renameable before publishing if Toby wants |
| GitHub owner | `Toby-Rogers` | Not the legacy `22TTodgers22` handle |

## Tone & scope rules

- **No emoji.** Senior hiring managers read emoji in code/docs as a junior-developer cue. The strategy doc was explicit about this.
- **Dry, specific, evidence-first.** No "powerful", "robust", "imagine if". State what something does.
- **The README is the artefact.** Most hiring managers won't clone — they skim the README. Write it accordingly when the time comes (architecture diagram, demo screenshot, "what's not in scope" section, link to LinkedIn, the 2× capacity metric quote from Toby's CV).
- **No new abstractions until there's a second use case.** Three similar lines beats premature abstraction.
- **Don't add tests, lint configs, CI, or pre-commit until they're earning their keep.** This is a weekend-shaped project, not a framework.

---

## File layout

```
atlassian-mcp/
├── .env.example                 # Template — copy to .env, fill in real values
├── .gitignore                   # .env excluded; do not commit secrets
├── README.md                    # Currently a WIP placeholder; the production version is the artefact
├── pyproject.toml               # Hatchling build, single console script `atlassian-mcp`
└── src/
    └── atlassian_mcp/
        ├── __init__.py
        ├── atlassian.py         # AtlassianClient — httpx + basic auth + REST calls
        └── server.py            # FastMCP server, tools registered with @mcp.tool()
```

## Tools

**Already wired:**
- `list_open_tickets_by_component(project_key, component, limit=25)` — JQL `project = X AND component = Y AND statusCategory != Done`, sorted priority then updated. Hits Jira's modern `/rest/api/3/search/jql` endpoint.

**Planned (per the strategy doc):**
- `summarise_recent_changes(project_key, days=7)` — recent changelog activity, formatted for narrative output
- `find_assets_referencing(query)` — Jira Assets / Insight lookup
- `generate_weekly_status_from_jira(project_key)` — closed-this-week tickets grouped by team, draft status update

When adding a new tool: write it in `server.py` decorated with `@mcp.tool()`, put the REST work in `atlassian.py` as a method on `AtlassianClient`. Keep the tool function thin.

---

## Operational notes

- **Run locally:** `uv sync` then `uv run atlassian-mcp`. The server waits on stdio — that's correct, it's how Claude Desktop talks to it.
- **Wire into Claude Desktop:** edit `%APPDATA%\Claude\claude_desktop_config.json` to register this server. The exact JSON to add can be generated when needed.
- **Atlassian sandbox:** if Toby doesn't want to point this at a live tenant, free dev sandboxes are available at atlassian.com.
- **Secrets:** `.env` is gitignored. Never commit credentials. Never echo the token in logs.
- **Git:** repo is initialised on `main`, no commits yet. Toby will commit when ready.
- **GitHub publish:** the local `gh` CLI on Toby's machine may still be authenticated as the legacy handle (`22TTodgers22`). Re-auth with `gh auth login` and pick `Toby-Rogers` before any `gh repo create`.

---

## Out of scope for this repo

- Write operations on Atlassian
- OAuth 3LO (note as production path in README)
- Tools beyond Jira and Confluence
- Anything that requires a backend service to host (this is stdio + local execution only)

---

*Last updated: 2026-05-08, end of scaffold session. Update when decisions change or new tools land.*
