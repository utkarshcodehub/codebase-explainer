import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.github_fetcher import parse_repo_url, fetch_repo_info, fetch_repo_tree, fetch_file_content
from services.file_selector import select_files, build_tree_string
from services.ai_explainer import explain_codebase

app = FastAPI(title="Codebase Explainer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExplainRequest(BaseModel):
    repo_url: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/explain")
async def explain_repo(req: ExplainRequest):
    # 1. Parse URL
    try:
        owner, repo = parse_repo_url(req.repo_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2. Fetch repo info
    try:
        repo_info = await fetch_repo_info(owner, repo)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Repository not found: {owner}/{repo}")

    # 3. Fetch tree
    branch = repo_info.get("default_branch", "main")
    try:
        tree = await fetch_repo_tree(owner, repo, branch)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch repo tree: {str(e)}")

    # 4. Select important files
    selected = select_files(tree)
    tree_string = build_tree_string(tree)

    # 5. Fetch file contents
    files = {}
    for item in selected:
        content = await fetch_file_content(owner, repo, item["path"], branch)
        if content:
            files[item["path"]] = content

    if not files:
        raise HTTPException(status_code=400, detail="Could not fetch any readable files from this repository")

    # 6. AI analysis
    try:
        analysis = explain_codebase(repo_info, tree_string, files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

    return {
        "repo_info": repo_info,
        "tree_string": tree_string,
        "files_analyzed": list(files.keys()),
        "analysis": analysis,
    }