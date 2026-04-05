# 📰 News Research Agent

A full-stack agentic AI application that takes a breaking news topic, autonomously searches the web for live articles, retrieves related content from a local vector database, drafts a structured editorial briefing, and flags conflicting information for human review.

Built to demonstrate agentic AI patterns — LangGraph state machines, RAG pipelines, and responsible AI design — in a real-world media context.

---

## How It Works

1. Enter a breaking news topic in the UI
2. The agent searches the web for current articles via Tavily
3. It queries a local ChromaDB archive for related stored stories
4. It synthesizes a structured editorial briefing using Claude
5. If conflicting claims are detected across sources, the briefing is flagged for editorial review
6. The result is returned to the UI with the full briefing, sources, and any conflict flags

---

## Architecture

```
User Input (topic)
      │
      ▼
┌─────────────────────────────────────────────┐
│              LangGraph Agent                │
│                                             │
│  [search] → [retrieve] → [synthesize]       │
│                               │             │
│                     needs_human_review?      │
│                        │           │        │
│                [human_review]     END        │
└─────────────────────────────────────────────┘
      │
      ▼
Editorial Briefing + Conflict Flags
```

### Agent Nodes

| Node | What it does |
|------|-------------|
| `search` | Web search for live articles using Tavily |
| `retrieve` | Semantic lookup against local ChromaDB archive |
| `synthesize` | Drafts structured briefing + detects conflicts via Claude |
| `human_review` | Formats conflict flags for editorial review |

The graph uses **conditional routing** — after `synthesize`, if conflicts were detected the graph routes to `human_review` before finishing. Otherwise it goes straight to `END`.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent orchestration | LangGraph |
| LLM | Anthropic Claude (claude-haiku-4-5) |
| Web search | Tavily API |
| Vector store | ChromaDB |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2, runs locally) |
| Backend API | FastAPI + Uvicorn |
| Frontend | React + TypeScript + Vite |

---

## Project Structure

```
news-agent/
├── backend/
│   ├── agents/
│   │   ├── state.py       # AgentState TypedDict — shared state across all nodes
│   │   ├── nodes.py       # search, retrieve, synthesize, human_review functions
│   │   └── graph.py       # LangGraph graph definition and compilation
│   ├── api/
│   │   ├── main.py        # FastAPI app, CORS, routing
│   │   └── routes/
│   │       ├── briefing.py  # POST /api/briefing
│   │       └── health.py    # GET /health
│   └── db/
│       └── retriever.py   # ChromaDB setup, ingest, and retrieval
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── SearchBar.tsx
│       │   ├── BriefingCard.tsx
│       │   └── LoadingSpinner.tsx
│       ├── hooks/
│       │   └── useBriefing.ts   # Async state management for API calls
│       ├── pages/
│       │   └── HomePage.tsx
│       └── types.ts             # Shared TypeScript interfaces
├── scripts/
│   └── seed_db.py         # Populates ChromaDB with sample news articles
└── .env.example
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Anthropic API key](https://console.anthropic.com) (for Claude)
- [Tavily API key](https://app.tavily.com) (free tier is sufficient)

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/news-agent.git
cd news-agent
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install langgraph langchain langchain-anthropic langchain-community anthropic tavily-python chromadb fastapi "uvicorn[standard]" pydantic python-dotenv httpx pandas tqdm sentence-transformers
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```
ANTHROPIC_API_KEY=sk-ant-...
TAVILY_API_KEY=tvly-...
CHROMA_PERSIST_DIR=./chroma_db
```

### 4. Seed the vector store

This downloads the embedding model (~90MB, one-time) and populates ChromaDB with 10 sample news articles:

```bash
# From the project root
python scripts/seed_db.py
```

### 5. Run the backend

```bash
# From the project root
uvicorn backend.api.main:app --reload
```

Backend runs at `http://localhost:8000`. Test it is alive at `http://localhost:8000/health`.

### 6. Run the frontend

Open a second terminal in the project root:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

---

## API

### `POST /api/briefing`

Run the agent on a topic and return an editorial briefing.

**Request:**
```json
{ "topic": "Federal Reserve interest rates" }
```

**Response:**
```json
{
  "topic": "Federal Reserve interest rates",
  "briefing": "...",
  "sources": ["https://..."],
  "conflict_flags": [
    {
      "claim_a": "...",
      "claim_b": "...",
      "source_a": "...",
      "source_b": "..."
    }
  ],
  "needs_human_review": true,
  "human_review_notes": "...",
  "latency_ms": 4200,
  "error": null
}
```

---

## Key Design Decisions

**Why LangGraph?** Standard LangChain chains are linear. LangGraph allows conditional routing between nodes based on state — essential for the `needs_human_review` branch. The `AgentState` TypedDict is the single source of truth that every node reads from and writes to.

**Why local embeddings?** Anthropic does not have an embeddings API. Rather than add an OpenAI dependency just for embeddings, `sentence-transformers` runs the embedding model fully locally — no extra API key, no cost per query, and the model is cached after the first download.

**Why Tavily?** It is the most LangChain-native web search tool, designed specifically for LLM agents. It returns clean, pre-extracted content rather than raw HTML, which makes it much easier for the synthesize node to reason over.

---

## License

MIT