import asyncio
from datetime import datetime
from memory import memory
from message import AgentMessage
from circuit_breaker import CircuitBreaker
from agents.web_agent import WebAgent
from agents.data_agent import DataAgent
from agents.scorer_agent import ScorerAgent
from agents.analysis_agent import AnalysisAgent
class Orchestrator:
    def __init__(self):
        self.web_agent = WebAgent(max_results=6)
        self.data_agent = DataAgent()
        self.scorer_agent = ScorerAgent()
        self.analysis_agent = AnalysisAgent()
        self.breakers = {
            "WebAgent": CircuitBreaker("WebAgent"),
            "DataAgent": CircuitBreaker("DataAgent"),
            "ScorerAgent": CircuitBreaker("ScorerAgent"),
            "AnalysisAgent": CircuitBreaker("AnalysisAgent")
        }
        print("[Orchestrator] Initialized - all agents ready")
    async def run(self, query: str) -> dict:
        """
        Main entry point.
        Takes a research query, runs full pipeline,
        returns structured result.
        """
        print(f"\n[Orchestrator] Starting research: '{query}'")
        web_result = await self._run_agent(
            agent=self.web_agent,
            breaker=self.breakers["WebAgent"],
            task="research",
            payload={"query": query},
            sender="Orchestrator",
            receiver="WebAgent"
        )
        if not web_result:
            return self._failed("WebAgent unavailable - circuit open")
        # Step 2 - DataAgent
        data_result = await self._run_agent(
            agent=self.data_agent,
            breaker=self.breakers["DataAgent"],
            task="enrich",
            payload=web_result.result,
            sender="WebAgent",
            receiver="DataAgent"
        )
        if not data_result:
            print("[Orchestrator] DataAgent unavailable - using raw web results")
            data_result = web_result
            data_result.result["sources"] = [
                {
                    "title": r["title"],
                    "url": r["url"],
                    "snippet": r.get("snippet", ""),
                    "content": r.get("snippet", ""),
                    "word_count": len(r.get("snippet", "").split())
                }
                for r in web_result.result.get("results", [])
            ]
        # Step 3 - ScorerAgent (Nim)
        scorer_result = await self._run_agent(
            agent=self.scorer_agent,
            breaker=self.breakers["ScorerAgent"],
            task="score",
            payload=data_result.result,
            sender="DataAgent",
            receiver="ScorerAgent"
        )
        if not scorer_result:
            print("[Orchestrator] ScoreAgent unavailable - using unranked sources")
            scorer_result = data_result
        analysis_result = await self._run_agent(
            agent=self.analysis_agent,
            breaker=self.breakers["AnalysisAgent"],
            task="analyze",
            payload=scorer_result.result,
            sender="ScorerAgent",
            receiver="AnalysisAgent"
        )
        if not analysis_result:
            return self._failed("AnalysisAgent unavailable - cannot complete the analysis")
        print(f"[Orchestrator] Research complete")
        return {
            "status": "success",
            "query": query,
            "synthesis": analysis_result.result["synthesis"],
            "insights": analysis_result.result["insights"],
            "source_count": len(scorer_result.result.get("sources", []))
        }
    async def _run_agent(
        self,
        agent,
        breaker: CircuitBreaker,
        task: str,
        payload: dict,
        sender: str,
        receiver: str
    ):
        """
        Runs an agent through its circuit breaker.
        Returns result on success, None if circuit is open or agent fails
        """
        if not breaker.can_proceed():
            print(f"[Orchestrator] {receiver} circuit is OPEN - skippimg")
            return None
        msg = AgentMessage(
            task=task,
            payload=payload,
            sender=sender,
            receiver=receiver
        )
        result = await agent.run(msg)
        if result.status == "success":
            breaker.record_success()
            return result
        else:
            breaker.record_failure()
            print(f"[Orchestrator] {receiver} failed: {result.error}")
            return None
    def _failed(self, reason: str) -> dict:
        return {"status": "failed", "reason": reason}
    
