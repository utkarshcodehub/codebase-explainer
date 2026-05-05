# Codebase Explainer

> Paste any code — a function, a class, an entire file — and get a plain-English explanation tailored to your experience level, with complexity analysis, potential bugs, and refactor suggestions.


---

## Overview

Reading unfamiliar code is one of the most time-consuming parts of software engineering — onboarding to a new codebase, reviewing a PR, or trying to understand a library's internals. Codebase Explainer acts as a senior engineer sitting next to you, explaining what the code does, why it's structured that way, what could go wrong, and how it could be improved.

Unlike generic "explain this code" prompts, this tool structures the explanation across multiple layers: high-level intent, line-by-line walkthrough, complexity, edge cases, and refactor opportunities.

---

## Features

- **Multi-language support** — Python, JavaScript, TypeScript, Java, C++, Go, Rust, SQL, and more
- **Explanation depth selector** — Beginner (what it does) / Intermediate (how it works) / Expert (why this approach)
- **Complexity analysis** — time and space complexity with reasoning
- **Bug & edge case detection** — spots null pointer risks, off-by-one errors, unhandled exceptions
- **Refactor suggestions** — concrete improvements with before/after examples
- **Concept extraction** — lists the CS concepts and patterns used in the code
- **Syntax highlighting** — proper code display with language-aware formatting

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite + Tailwind CSS |
| Backend | FastAPI (Python) |
| AI | Groq API — Llama 3.3 70B |
| Deployment | Vercel (frontend) + Render (backend) |

---

## Architecture

```
User pastes code + selects language + selects depth
        ↓
Frontend → POST /explain (FastAPI)
        ↓
Groq LLM → multi-section structured explanation
        ↓
JSON response → Frontend renders tabbed explanation panels
```

---

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### Environment Variables

**Backend `.env`:**
```
GROQ_API_KEY=your_groq_api_key
```

**Frontend `.env`:**
```
VITE_API_URL=http://localhost:8000
```

---

## API

### `POST /explain`

**Request:**
```json
{
  "code": "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)",
  "language": "python",
  "depth": "intermediate"
}
```

**Response:**
```json
{
  "summary": "A recursive divide-and-conquer sorting algorithm that splits the array in half, sorts each half, then merges them.",
  "walkthrough": [
    {"line": "if len(arr) <= 1", "explanation": "Base case: arrays of 0 or 1 elements are already sorted"},
    {"line": "mid = len(arr) // 2", "explanation": "Find the midpoint using integer division"}
  ],
  "time_complexity": "O(n log n)",
  "space_complexity": "O(n) — due to auxiliary arrays created during merge",
  "concepts_used": ["Recursion", "Divide and Conquer", "Merge operation"],
  "potential_bugs": ["Missing merge() function definition", "Creates new arrays at each level — not in-place"],
  "refactor_suggestions": ["Implement as in-place merge sort to reduce space to O(log n)", "Add type hints for clarity"]
}
```

---

## Supported Languages

Python · JavaScript · TypeScript · Java · C++ · C · Go · Rust · Ruby · PHP · Swift · Kotlin · SQL · Bash · R

---

## Project Structure

```
codebase-explainer/
├── backend/
│   ├── main.py
│   ├── routers/
│   │   └── explain.py
│   ├── services/
│   │   └── ai.py
│   └── requirements.txt
└── frontend/
    └── src/
        ├── App.jsx
        └── components/
            ├── CodeInput.jsx
            ├── ExplanationPanel.jsx
            ├── ComplexityBadge.jsx
            └── RefactorSuggestions.jsx
```

---

