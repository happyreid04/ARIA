import asyncio
from message import AgentMessage
from agents.web_agent import WebAgent
async def main():
    msg = AgentMessage(
        task="test web search",
        payload={"query": "AI agents infrastructure in 2026"},
        sender="human",
        receiver="WebAgent"
    )
    agent = WebAgent(max_results=3)
    result = await agent.run(msg)
    print(f"\nStatus: {result.status}")
    if result.status == "success":
        print(f"Query: {result.result['query']}")
        print(f"n\Results:")
        for i, r in enumerate(result.result['results'], 1):
            print(f"{i}. {r['title']} - {r['href']}")
            print(f"   {r['url']}\n")
            print(f"  {r['snippet'][:100]}...")
        else:
            print(f"Error: {result.result}")
if __name__ == "__main__":
    asyncio.run(main())
    

