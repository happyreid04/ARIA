# test_phase8.py
# Tests memory — run twice, second run should hit cache

import asyncio
from orchestrator import Orchestrator


async def main():
    orchestrator = Orchestrator()
    query = "AI agent infrastructure site:arxiv.org OR site:hackernoon.com"

    # first run — full pipeline
    print("=" * 60)
    print("RUN 1 — Fresh research")
    print("=" * 60)
    result1 = await orchestrator.run(query)
    print(f"Status: {result1['status']}")
    print(f"Tokens used: {result1.get('tokens_used', 0)}")

    # second run — should hit memory
    print("\n" + "=" * 60)
    print("RUN 2 — Should return from memory")
    print("=" * 60)
    result2 = await orchestrator.run(query)
    print(f"Status: {result2['status']}")
    print(f"Tokens used: {result2.get('tokens_used', 0)}")

    # force refresh — bypasses memory
    print("\n" + "=" * 60)
    print("RUN 3 — Force refresh, bypasses memory")
    print("=" * 60)
    result3 = await orchestrator.run(query, force_refresh=True)
    print(f"Status: {result3['status']}")
    print(f"Tokens used: {result3.get('tokens_used', 0)}")

    # list all memories
    print("\n" + "=" * 60)
    print("ARIA MEMORY — All past research")
    print("=" * 60)
    memories = orchestrator.memory.list_memories()
    for m in memories:
        print(f"  Query: {m['query']}")
        print(f"  When: {m['timestamp']}")
        print(f"  Accessed: {m['access_count']} times")


if __name__ == "__main__":
    asyncio.run(main())
