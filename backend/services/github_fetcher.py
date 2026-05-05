import httpx
import base64
import os
from typing import Optional

GITHUB_API = "https://api.github.com"

def _headers() -> dict:
    token = os.getenv("GITHUB_TOKEN")
    h = {"Accept": "application/vnd.github.v3+json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def parse_repo_url(url: str) -> tuple[str, str]:
    """Extract owner/repo from various GitHub URL formats."""
    url = url.strip().rstrip("/")
    if url.startswith("https://github.com/"):
        parts = url.replace("https://github.com/", "").split("/")
    elif url.startswith("github.com/"):
        parts = url.replace("github.com/", "").split("/")
    else:
        parts = url.split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL. Use format: https://github.com/owner/repo")
    return parts[0], parts[1]


async def fetch_repo_info(owner: str, repo: str) -> dict:
    """Fetch basic repo metadata."""
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(f"{GITHUB_API}/repos/{owner}/{repo}", headers=_headers())
        resp.raise_for_status()
        data = resp.json()
        return {
            "name": data["name"],
            "full_name": data["full_name"],
            "description": data.get("description", ""),
            "language": data.get("language", "Unknown"),
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "topics": data.get("topics", []),
            "default_branch": data.get("default_branch", "main"),
        }


async def fetch_repo_tree(owner: str, repo: str, branch: str = "main") -> list[dict]:
    """Fetch full recursive tree of the repo."""
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1",
            headers=_headers(),
        )
        resp.raise_for_status()
        tree = resp.json().get("tree", [])
        return [
            {"path": item["path"], "type": item["type"], "size": item.get("size", 0)}
            for item in tree
        ]


async def fetch_file_content(owner: str, repo: str, path: str, branch: str = "main") -> Optional[str]:
    """Fetch a single file's content (decoded from base64)."""
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}?ref={branch}",
            headers=_headers(),
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        if data.get("encoding") == "base64" and data.get("content"):
            try:
                return base64.b64decode(data["content"]).decode("utf-8", errors="replace")
            except Exception:
                return None
        return None
