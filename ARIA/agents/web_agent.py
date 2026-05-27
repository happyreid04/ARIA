from ddgs import DDGS
from agents.base_agent import BaseAgent
from message import AgentMessage
class WebAgent(BaseAgent):
    def __init__(self, max_results: int = 5):
        super().__init__(name="WebAgent")
        self.max_results = max_results
    async def run(self, message: AgentMessage) -> AgentMessage:
        query = message.payload.get("query")
        if not query:
            return message.fail("No query provided in payload.")
        self.log(f"Searching: '{query}'")
        try:
            results = self._search(query)
            self.log(f"Found {len(results)} results")
            return message.succeed({"query": query, "results": results})
        except Exception as e:
            return message.fail(f"Search failed: {e}")
    def _search(self, query: str) -> list:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=self.max_results):
                results.append({
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "body": r.get("body")
                })
            return results
        

