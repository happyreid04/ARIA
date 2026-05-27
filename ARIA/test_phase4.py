import asyncio
from message import AgentMessage
from agents.web_agent import WebAgent
from agents.data_agent import DataAgent
from agents.analysis_agent import AnalysisAgent
async def main():
    query = "AI agents infrastucture 2026"
    web_msg = AgentMessage(
        task='research',
        payload={'query': query},
        sender="human",
        receiver="WebAgent"
    )
    web_agent = WebAgent(max_results=3)
    web_result = await web_agent.run(web_msg)
    if web_result.status != "success":
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
    if data_result.status !="success":
        print(f"DataAgent failed: {data_result.error}")
        return
    analysis_msg = AgentMessage(
        task="analyze",
        payload=data_result.result,
        sender="DataAgent",
        receiver="AnalysisAgent"
    )
    analysis_agent = AnalysisAgent()
    analysis_result = await analysis_agent.run(analysis_msg)
    print(f"\nStatus: {analysis_result.status}")
    if analysis_result.status == "success":
        result = analysis_result.result
        print(f"\nQuery: {result['query']}")
        print(f"\n--- Individual Insights ---")
        for i, insight in enumerate(result['insights'], 1):
            print(f"\nSource {i}: {insight['title']}")
            print(insight['raw_analysis'])
        print(f"\n-- Synthesis ---")
        print(result['synthesis'])
    else:
        print(f"Error: {analysis_result.error}")
if __name__ == "__main__":
    asyncio.run(main())


