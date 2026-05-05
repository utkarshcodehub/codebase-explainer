"""
Smart file selector — picks the most important files from a repo tree
for AI analysis. Prioritizes entry points, configs, and core logic.
"""

# High-priority filenames (exact match)
HIGH_PRIORITY_FILES = {
    "package.json", "pyproject.toml", "setup.py", "setup.cfg",
    "cargo.toml", "go.mod", "pom.xml", "build.gradle",
    "dockerfile", "docker-compose.yml", "docker-compose.yaml",
    "makefile", ".env.example", "requirements.txt",
    "readme.md", "readme.rst",
    "app.py", "main.py", "index.py", "server.py", "wsgi.py", "asgi.py",
    "index.js", "index.ts", "app.js", "app.ts", "server.js", "server.ts",
    "main.go", "main.rs", "lib.rs",
    "vite.config.js", "vite.config.ts", "next.config.js", "next.config.ts",
    "webpack.config.js", "tsconfig.json", "tailwind.config.js",
    "manage.py", "settings.py", "urls.py", "models.py", "views.py",
}

# Directory patterns to SKIP
SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", ".next", "dist", "build",
    "vendor", ".venv", "venv", "env", ".tox", "target",
    "coverage", ".nyc_output", ".pytest_cache", ".mypy_cache",
    "assets", "static/images", "public/images", "migrations",
    ".github", ".vscode", ".idea",
}

# File extensions worth reading
CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java",
    ".rb", ".php", ".swift", ".kt", ".scala", ".c", ".cpp", ".h",
    ".vue", ".svelte", ".astro",
    ".json", ".toml", ".yaml", ".yml",
    ".md", ".rst", ".txt",
    ".sql", ".graphql", ".gql", ".prisma",
    ".css", ".scss", ".less",
    ".html", ".ejs", ".hbs",
    ".sh", ".bash",
    ".env.example",
}

# Skip patterns in filenames
SKIP_PATTERNS = {
    "test_", "_test.", ".test.", ".spec.", "test.", "spec.",
    "mock", "fixture", "snapshot",
    ".min.", ".map", ".lock",
    "license", "changelog", "contributing",
}

MAX_FILE_SIZE = 50_000  # 50KB max per file
MAX_FILES = 15


def _should_skip_path(path: str) -> bool:
    parts = path.lower().split("/")
    for part in parts[:-1]:  # check directories
        if part in SKIP_DIRS:
            return True
    return False


def _should_skip_file(filename: str) -> bool:
    lower = filename.lower()
    for pattern in SKIP_PATTERNS:
        if pattern in lower:
            return True
    return False


def _get_extension(filename: str) -> str:
    if "." in filename:
        return "." + filename.rsplit(".", 1)[-1].lower()
    # Handle extensionless files like Dockerfile, Makefile
    lower = filename.lower()
    if lower in {"dockerfile", "makefile", "procfile", "gemfile", "rakefile"}:
        return ".special"
    return ""


def _priority_score(item: dict) -> int:
    """Higher score = more important."""
    path = item["path"]
    filename = path.split("/")[-1].lower()
    depth = path.count("/")
    score = 0

    # Exact filename match
    if filename in HIGH_PRIORITY_FILES:
        score += 100

    # Root-level files are more important
    if depth == 0:
        score += 30
    elif depth == 1:
        score += 20
    elif depth == 2:
        score += 10

    # Src directory files get a boost
    parts = path.lower().split("/")
    if "src" in parts or "lib" in parts or "app" in parts or "core" in parts:
        score += 15

    # Config files
    if filename.endswith((".json", ".toml", ".yaml", ".yml")) and depth <= 1:
        score += 20

    # Entry-point-like names
    entry_names = {"main", "index", "app", "server", "routes", "api", "config", "models", "schema", "database", "db"}
    name_without_ext = filename.rsplit(".", 1)[0] if "." in filename else filename
    if name_without_ext in entry_names:
        score += 25

    return score


def select_files(tree: list[dict]) -> list[dict]:
    """Select the most important files from a repo tree."""
    candidates = []

    for item in tree:
        if item["type"] != "blob":
            continue
        path = item["path"]
        filename = path.split("/")[-1]

        # Skip unwanted dirs
        if _should_skip_path(path):
            continue

        # Skip test/lock files
        if _should_skip_file(filename):
            continue

        # Check extension
        ext = _get_extension(filename)
        if ext not in CODE_EXTENSIONS and ext != ".special":
            continue

        # Skip huge files
        if item.get("size", 0) > MAX_FILE_SIZE:
            continue

        score = _priority_score(item)
        candidates.append({**item, "score": score})

    # Sort by score descending, take top N
    candidates.sort(key=lambda x: x["score"], reverse=True)
    selected = candidates[:MAX_FILES]

    return [{"path": f["path"], "size": f.get("size", 0)} for f in selected]


def build_tree_string(tree: list[dict], max_lines: int = 80) -> str:
    """Build a visual tree string from the repo tree (directories + files)."""
    # Filter out skipped dirs and limit depth
    lines = []
    for item in tree:
        if _should_skip_path(item["path"]):
            continue
        depth = item["path"].count("/")
        if depth > 3:
            continue
        prefix = "  " * depth
        name = item["path"].split("/")[-1]
        if item["type"] == "tree":
            lines.append(f"{prefix}{name}/")
        else:
            lines.append(f"{prefix}{name}")
        if len(lines) >= max_lines:
            lines.append("  ... (truncated)")
            break
    return "\n".join(lines)
