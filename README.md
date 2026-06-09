# ARIA
a research tool that communicates with several agents , written in python and nim


# ARIA — Autonomous Research Intelligence Architecture

> 🚧 **Active Development — Phase 8 of 10 complete**  
> Built in public. Progress updated regularly.

ARIA is a multi-agent research system built in Python and Nim, designed to autonomously search, collect, score, and analyse information through a coordinated network of specialized agents — all orchestrated by a fault-tolerant brain layer.

---

## Architecture

```
WebAgent          — searches and retrieves web content
     ↓
DataAgent         — collects and structures raw data
     ↓
ScorerAgent       — scores and ranks data (Nim via nimpy)
     ↓
AnalysisAgent     — deep analysis via Cerebras LLM
     ↓
Orchestrator      — agent brain with Circuit Breaker pattern
```

---

## Agent Breakdown

| Agent | Language | Role |
|---|---|---|
| WebAgent | Python | Web search and content retrieval |
| DataAgent | Python | Raw data collection and structuring |
| ScorerAgent | Nim via nimpy | High-performance numeric scoring and ranking |
| AnalysisAgent | Python + Cerebras LLM | Deep intelligence analysis and classification |
| Orchestrator | Python | Central brain — coordinates all agents, circuit breaker fault tolerance |

---

## Stack

| Layer | Technology | Purpose |
|---|---|---|
| Core agents | Python | Agent logic and communication |
| Performance layer | Nim + nimpy | Fast numeric scoring — native speed inside Python |
| LLM | Cerebras + LLM | Research analysis and classification |
| Orchestration | Python asyncio | Agent coordination and decision loop |
| Fault tolerance | Circuit Breaker | Prevents cascade failures across agents |

---

## Build Roadmap

### ✅ Completed Phases

- **Phase 1** — Agent communication layer — verified inter-agent messaging works
- **Phase 2** — WebAgent — web search integration and content retrieval
- **Phase 3** — DataAgent — data collection pipeline from web sources
- **Phase 4** — ScorerAgent — Nim-powered numeric scoring via nimpy bridge
- **Phase 5** — AnalysisAgent — Cerebras LLM integration for deep analysis
- **Phase 6** — Orchestrator — central brain with Circuit Breaker pattern

### 🔄 Upcoming Phases

- **Phase 7** — WriterAgent — structured report generation from analysis output
- **Phase 8** — Memory layer — persistent agent memory across sessions
- **Phase 9** — CLI — command line interface for direct interaction
- **Phase 10** — Deploy — cloud deployment for 24/7 autonomous operation

---

## Why Nim + Python

Most agent systems are pure Python. ARIA uses Nim for the ScorerAgent via nimpy — giving native compiled speed for numeric processing without leaving the Python ecosystem. This matters at scale when scoring hundreds of data points per cycle.

---

## Project Structure

```
ARIA/
├── agents/
│   ├── web_agent.py          # Web search and retrieval
│   ├── data_agent.py         # Data collection and structuring
│   ├── scorer_agent.nim      # Nim scoring logic
│   └── analysis_agent.py     # LLM-powered analysis
├── orchestrator.py           # Central brain + circuit breaker
├── .gitignore
└── README.md
```

---

## Status

| Phase | Status |
|---|---|
| Agent communication | ✅ Done |
| Web search | ✅ Done |
| Data collection | ✅ Done |
| Nim scoring | ✅ Done |
| LLM analysis | ✅ Done |
| Orchestration + Circuit Breaker | ✅ Done |
| Writer agent | 🔄 In progress |
| Memory layer | ⏳ Planned |
| CLI | ⏳ Planned |
| Deploy | ⏳ Planned |

---

## Author

**happyreid04**

**Feel free to sponsor with stars ⭐⭐**

---

## License

MIT
