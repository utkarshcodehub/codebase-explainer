import os
import json
from groq import Groq

client = None

def get_client():
    global client
    if client is None:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return client


SYSTEM_PROMPT = """You are a senior software engineer who explains codebases clearly.
Given a GitHub repository's structure and key file contents, produce a comprehensive explanation.

You MUST respond with valid JSON only — no markdown, no backticks, no extra text.

JSON schema:
{
  "tech_stack": [
    {"name": "string", "category": "language|framework|database|devops|styling|testing|other", "confidence": "confirmed|likely"}
  ],
  "architecture_summary": "2-3 paragraph overview of the architecture and design patterns used",
  "entry_points": [
    {"file": "path/to/file", "purpose": "what this entry point does"}
  ],
  "file_relationships": [
    {"from": "file_a", "to": "file_b", "relationship": "imports|configures|routes_to|extends|uses"}
  ],
  "key_modules": [
    {"path": "path/to/file_or_dir", "role": "what this module/file is responsible for", "importance": "critical|important|supporting"}
  ],
  "mermaid_diagram": "A valid Mermaid flowchart (graph TD) showing the architecture. Use simple node IDs (A, B, C...) with labels. Keep it under 15 nodes. NO special characters in labels — only alphanumeric, spaces, and hyphens.",
  "onboarding_guide": {
    "start_here": "Which file to read first and why",
    "reading_order": ["ordered list of files/dirs to read"],
    "key_concepts": ["list of domain concepts a new dev should understand"],
    "common_tasks": [
      {"task": "description of common task", "files": ["relevant files"]}
    ]
  },
  "complexity_rating": {
    "score": 1-10,
    "reasoning": "why this rating"
  }
}
"""


MAX_TOTAL_CHARS = 25000  # ~6K tokens, safe for Groq limits
MAX_PER_FILE_CHARS = 2000


def build_prompt(repo_info: dict, tree_string: str, files: dict[str, str]) -> str:
    # Truncate tree if too long
    if len(tree_string) > 3000:
        tree_string = tree_string[:3000] + "\n... (truncated)"

    # Budget: reserve space for tree + metadata + system prompt
    overhead = len(tree_string) + 1500
    budget = MAX_TOTAL_CHARS - overhead

    files_section = ""
    for path, content in files.items():
        # Truncate individual files
        if len(content) > MAX_PER_FILE_CHARS:
            content = content[:MAX_PER_FILE_CHARS] + "\n... (truncated)"
        
        entry = f"\n--- FILE: {path} ---\n{content}\n"
        
        # Stop adding files if we'd exceed budget
        if len(files_section) + len(entry) > budget:
            break
        files_section += entry

    return f"""Analyze this GitHub repository:

REPO: {repo_info['full_name']}
DESCRIPTION: {repo_info.get('description', 'N/A')}
PRIMARY LANGUAGE: {repo_info.get('language', 'Unknown')}
STARS: {repo_info.get('stars', 0)}
TOPICS: {', '.join(repo_info.get('topics', []))}

DIRECTORY STRUCTURE:
{tree_string}

KEY FILES:
{files_section}

Produce the JSON analysis now."""


def explain_codebase(repo_info: dict, tree_string: str, files: dict[str, str]) -> dict:
    prompt = build_prompt(repo_info, tree_string, files)

    response = get_client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=4000,
        response_format={"type": "json_object"},
    )

    text = response.choices[0].message.content.strip()

    # Clean potential markdown fences
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]

    return json.loads(text)