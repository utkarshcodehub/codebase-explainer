import os
import json
from groq import Groq

client = None

def get_client():
    global client
    if client is None:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return client


SYSTEM_PROMPT = """You are a Principal Software Architect specializing in automated codebase analysis and technical documentation.

TASK:
Analyze the provided GitHub repository structure and file contents to generate a precise, actionable visual and structural analysis.

OUTPUT CONSTRAINTS:
- Output MUST be valid, parseable raw JSON.
- DO NOT wrap the output in Markdown code blocks (e.g., no ```json ... ```).
- Output NO introductory, conversational, or concluding text outside the JSON object.
- Escape all special characters inside string values properly (e.g., use \\" for double quotes, \\n for line breaks).

ANALYSIS GUIDELINES:
1. Grounding: Rely strictly on provided repository metadata and files. If a file or pattern is not explicitly visible, do not speculate.
2. Architecture & Relationships: Capture exact file paths and meaningful dependency/flow relationships. Avoid trivial or redundant relationships.
3. Mermaid Rules:
   - Output valid Mermaid.js flowchart syntax using `graph TD`.
   - Use simple alphanumeric IDs for nodes (e.g., `node1`, `node2`).
   - Wrap labels in explicit double quotes inside square brackets: `node1["Label Text"]`.
   - Do NOT use special symbols, unescaped quotes, nested brackets, or parentheses inside label text. Keep labels concise (< 30 characters).
   - Maximum 15 nodes. Focus on high-level system boundaries and primary data flows.

JSON SCHEMA:
{
  "tech_stack": [
    {
      "name": "string",
      "category": "language|framework|database|devops|styling|testing|other",
      "confidence": "confirmed|likely"
    }
  ],
  "architecture_summary": "2-3 concise paragraphs detailing the actual system architecture, primary data flow, state management, and design patterns used.",
  "entry_points": [
    {
      "file": "path/to/file",
      "purpose": "Precise responsibility of this entry point"
    }
  ],
  "file_relationships": [
    {
      "from": "path/to/file_a",
      "to": "path/to/file_b",
      "relationship": "imports|configures|routes_to|extends|uses"
    }
  ],
  "key_modules": [
    {
      "path": "path/to/file_or_dir",
      "role": "Specific architectural role and responsibility",
      "importance": "critical|important|supporting"
    }
  ],
  "mermaid_diagram": "graph TD\\n  A[\\\"Client App\\\"] --> B[\\\"API Router\\\"]",
  "onboarding_guide": {
    "start_here": "Exact file to inspect first and why it sets up the system context",
    "reading_order": [
      "ordered path/to/file strings"
    ],
    "key_concepts": [
      "Domain concepts or specific architectural mechanics essential for a developer"
    ],
    "common_tasks": [
      {
        "task": "Description of a frequent developer task (e.g., adding a route, modifying schema)",
        "files": [
          "relevant/file/paths"
        ]
      }
    ]
  },
  "complexity_rating": {
    "score": 1,
    "reasoning": "Concrete analysis explaining why this codebase receives a 1-10 rating based on coupling, modularity, and abstraction scale"
  }
}"""


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
        model="openai/gpt-oss-120b",
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