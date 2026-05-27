import asyncio
from message import AgentMessage
from agents.web_agent import WebAgent
from agents.data_agent import DataAgent
from agents.scorer_agent import ScorerAgent
from agents.analysis_agent import AnalysisAgent
async def main():
    query = "AI agents infrastucture 2026"
    web_msg = AgentMessage(
        task="research",
        payload={"query": query},
        sender="human",
        receiver="WebAgent"
    )
    web_agent = WebAgent(max_results=3)
    web_result = await web_agent.run(web_msg)
    if web_result.status !="success":
        print(f"WebAgent failed: {web_result.error}")
        return
    data_msg = AgentMessage(
        task="enrich",
        payload=web_result.result,
        sender="WebAgent",
        receiver="DataAgent"
    )
    data_agent = DataAgent()
    data_result = await data_agent.run(data_msg)
    if data_result.status != "success":
        print(f"DataAgent failed: {data_result.error}")
        return
    scorer_msg = AgentMessage(
        task="score",
        payload=data_result.result,
        sender="DataAgent",
        receiver="ScorerAgent"
    )
    scorer_agent = ScorerAgent()
    scorer_result = await scorer_agent.run(scorer_msg)
    if scorer_result.status != "success":
        print(f"ScorerAgent failed: {scorer_result.error}")
        return
    analysis_msg = AgentMessage(
        task="analyze",
        payload=scorer_result.result,
        sender="ScorerAgent",
        receiver="AnalysisAgent"
    )
    analysis_agent = AnalysisAgent()
    analysis_result = await analysis_agent.run(analysis_msg)
    print(f"\nStatus: {analysis_result.status}")
    if analysis_result.status == "success":
        result = analysis_result.result
        print(f"\nQuery: {result['query']}")
        print(f"\n--- Synthesis ---")
        print(result['synthesis'])
    else:
        print(f"Error: {analysis_result.error}")
if __name__ == "__main__":
    asyncio.run(main())