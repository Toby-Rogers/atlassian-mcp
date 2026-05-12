# Repo file reference

A file-by-file rundown of what each thing in this repo is and why it exists. Skips `.git/`, `.venv/`, and `__pycache__/` — those are tool-managed and not yours to edit.

---

## Project files (hand-written, source-controlled)

### `CLAUDE.md`
Briefing for any future Claude Code session. Locked decisions (Python, FastMCP, API-token auth, read-only), tone rules (no emoji), file layout, scope boundaries. The "why" doc so a fresh session doesn't re-litigate choices.

### `README.md`
Public-facing artefact. The thing hiring managers will actually skim on GitHub. Polished with the 2× metric, architecture diagram, and demo screenshot.

### `pyproject.toml`
Python package manifest. Declares:
- Package name (`atlassian-mcp`) and version
- Python version requirement (≥3.11)
- Three runtime dependencies: `mcp[cli]`, `httpx`, `python-dotenv`
- The `atlassian-mcp` console script entry point → `atlassian_mcp.server:main`
- Hatchling as the build backend

### `.env.example`
Template for the three secrets the server needs at runtime:
- `ATLASSIAN_BASE_URL`
- `ATLASSIAN_EMAIL`
- `ATLASSIAN_API_TOKEN`

Copy this to `.env` and fill in real values.

### `.env`
Your actual credentials. **Gitignored.** Never commit.

### `.gitignore`
Standard Python excludes plus `.env` and `uv.lock`.

---

## Source code

### `src/atlassian_mcp/__init__.py`
Exposes `__version__ = "0.1.0"`. Marks the directory as a Python package.

### `src/atlassian_mcp/atlassian.py`
The REST layer. `AtlassianClient` dataclass:
- Loads creds from environment variables
- Builds an async `httpx` client with basic auth
- One method so far: `search_jira(jql, limit)` — hits `/rest/api/3/search/jql` and reshapes the response into a flat list of dicts (`key`, `summary`, `status`, `priority`, `assignee`, `updated`)

### `src/atlassian_mcp/server.py`
The MCP layer. Responsibilities:
- Instantiates `FastMCP("atlassian-mcp")`
- Registers the one tool (`list_open_tickets_by_component`) which builds a JQL string and delegates to the client
- Exposes `main()` for the console script entry point

This is the file Claude Desktop actually launches over stdio.

---

## Tool-managed files (you didn't write these, but they affect behaviour)

### `uv.lock`
Lockfile produced by `uv sync`. Pins the exact version + hash of every transitive dependency (httpx, pydantic, anyio, …) so any machine running `uv sync` gets an identical environment.

- `pyproject.toml` says: "I want httpx ≥0.27"
- `uv.lock` says: "specifically httpx 0.28.1 with this sha256"

Currently gitignored — fine for a demo. In a team/prod setting you'd usually commit it for reproducible installs.

### `.venv/`
The virtualenv `uv` created. Contains the Python interpreter copy and every installed package. Disposable — `uv sync` rebuilds it from `pyproject.toml` + `uv.lock`. Never commit, never edit by hand.

### `.git/`
Git's internal storage. Ignore.

---

## What's notably absent

Per `CLAUDE.md`'s "don't add it until it earns its keep" rule, this repo has no:
- `tests/`
- CI workflow
- Linter config
- Pre-commit hooks

Deliberate for a weekend portfolio piece. Add them when there's a real reason to.

---

## docs/

### `docs/demo.png`
Screenshot used in the README to show the server working against Claude Desktop.

### `docs/file-reference.md`
This document.
