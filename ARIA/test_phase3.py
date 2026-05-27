import asyncio
from message import AgentMessage
from agents.web_agent import WebAgent
from agents.data_agent import DataAgent
async def main():
    # Step 1: WebAgent search
    web_msg = AgentMessage(
        task="test web search",
        payload={"query": "AI agents infrastructure in 2026"},
        sender="human",
        receiver="WebAgent"
    )
    web_agent = WebAgent(max_results=3)
    web_result = await web_agent.run(web_msg)
    print(f"\nWebAgent Status: {web_result.status}")
    if web_result.status == "success":
        print(f"WebAgent Query: {web_result.result['query']}")
        print(f"WebAgent Results:")
        for i, r in enumerate(web_result.result['results'], 1):
            print(f"{i}. {r['title']} - {r['href']}")
            print(f"   {r['url']}\n")
            print(f"  {r['snippet'][:100]}...")
    else:
        print(f"WebAgent Error: {web_result.result}")
        return
    # Step 2: DataAgent enrichment
    data_msg = AgentMessage(
        task="enrich web results",
        payload={
            "query": web_result.result['query'],
            "results": web_result.result['results']
        },
        sender="WebAgent",
        receiver="DataAgent"
    )
    data_agent = DataAgent()
    data_result = await data_agent.run(data_msg)
    print(f"\nDataAgent Status: {data_result.status}")
    if data_result.status == "success":
        print(f"DataAgent Enriched Sources:")
        for i, s in enumerate(data_result.result['sources'], 1):
            print(f"{i}. {s['title']} - {s['url']}")
            print(f"   Word Count: {s['word_count']}")
            print(f"   Snippet: {s['snippet'][:100]}...")
            print(f"   Content Preview: {s['content'][:200]}...\n")
    else:
        print(f"DataAgent Error: {data_result.result}")
if __name__ == "__main__":
    asyncio.run(main())