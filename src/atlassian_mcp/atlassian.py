import os
from dataclasses import dataclass
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


@dataclass
class AtlassianClient:
    base_url: str
    email: str
    api_token: str

    @classmethod
    def from_env(cls) -> "AtlassianClient":
        return cls(
            base_url=os.environ["ATLASSIAN_BASE_URL"].rstrip("/"),
            email=os.environ["ATLASSIAN_EMAIL"],
            api_token=os.environ["ATLASSIAN_API_TOKEN"],
        )

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            auth=(self.email, self.api_token),
            timeout=30.0,
            headers={"Accept": "application/json"},
        )

    async def search_jira(self, jql: str, limit: int = 25) -> list[dict]:
        async with self._client() as http:
            r = await http.post(
                f"{self.base_url}/rest/api/3/search/jql",
                json={
                    "jql": jql,
                    "maxResults": limit,
                    "fields": ["summary", "status", "priority", "assignee", "updated"],
                },
            )
            r.raise_for_status()
            return [
                {
                    "key": issue["key"],
                    "summary": issue["fields"]["summary"],
                    "status": issue["fields"]["status"]["name"],
                    "priority": (issue["fields"].get("priority") or {}).get("name"),
                    "assignee": (issue["fields"].get("assignee") or {}).get("displayName"),
                    "updated": issue["fields"]["updated"],
                }
                for issue in r.json().get("issues", [])
            ]

    async def recently_resolved(
        self,
        project_key: str,
        days: int = 7,
    ) -> list[dict]:
        jql = (
            f'project = "{project_key}" '
            'AND statusCategory = Done '
            f'AND resolved >= -{days}d '
            'ORDER BY resolved DESC'
        )
        async with self._client() as http:
            r = await http.post(
                f"{self.base_url}/rest/api/3/search/jql",
                json={
                    "jql": jql,
                    "maxResults": 100,
                    "fields": [
                        "summary",
                        "priority",
                        "assignee",
                        "resolutiondate",
                        "components",
                    ],
                },
            )
            r.raise_for_status()
            return [
                {
                    "key": issue["key"],
                    "summary": issue["fields"]["summary"],
                    "priority": (issue["fields"].get("priority") or {}).get("name"),
                    "assignee": (issue["fields"].get("assignee") or {}).get("displayName"),
                    "resolved": issue["fields"].get("resolutiondate"),
                    "components": [
                        c["name"] for c in (issue["fields"].get("components") or [])
                    ],
                }
                for issue in r.json().get("issues", [])
            ]
