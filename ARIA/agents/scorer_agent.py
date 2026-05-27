import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scorer import rankSources
from agents.base_agent import BaseAgent
from message import AgentMessage
class ScorerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ScorerAgent")
    async def run(self, message: AgentMessage) -> AgentMessage:
        sources = message.payload.get("sources")
        query = message.payload.get("query")
        if not sources:
            return message.fail("No sources to score")
        self.log(f"Scoring {len(sources)} sources via Nim")
        word_counts = [s.get("word_count", 0) for s in sources]
        snippet_lens = [len(s.get("snippet", "")) for s in sources]
        title_lens = [len(s.get("title", "")) for s in sources]
        scores = rankSources(word_counts, snippet_lens, title_lens)
        for i, source in enumerate(sources):
            source["relevance_score"] = round(scores[i], 4)
        ranked = sorted(sources, key=lambda x: x["relevance_score"], reverse=True)
        self.log(f"Ranking complete:")
        for i, s in enumerate(ranked, 1):
            self.log(f" {i}. [{s['relevance_score']}] {s['title']}")
        return message.succeed({
            "query": query,
            "sources": ranked,
        })