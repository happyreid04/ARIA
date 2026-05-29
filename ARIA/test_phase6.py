import asyncio
from orchestrator import Orchestrator
async def main():
    orchestrator = Orchestrator()
    result = await orchestrator.run(
        "AI agent infrastructure site:dev.to OR site:medium.com"
    )
    print(f"\nStatus: {result['status']}")
    if result['status'] == "success":
        print(f"Query: {result['query']}")
        print(f"Sources used: {result['source_count']}")
        print(f"\n--- Final Synthesis ---")
        print(result['synthesis'])
    else:
        print(f"Failed: {result['reason']}")
if __name__ == "__main__":
    asyncio.run(main())
