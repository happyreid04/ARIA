# test_phase7.py
import asyncio
from orchestrator import Orchestrator


async def main():
    orchestrator = Orchestrator()

    result = await orchestrator.run(
        "AI agent infrastructure site:arxiv.org OR site:hackernoon.com"
    )

    print(f"\nStatus: {result['status']}")

    if result['status'] == 'success':
        print(f"\n{'='*60}")
        print(result['report'])
        print(f"{'='*60}")
        print(f"\nTokens used: {result.get('tokens_used', 0)}")
        print(f"Generated at: {result.get('generated_at', '')}")
    else:
        print(f"Failed: {result['reason']}")


if __name__ == "__main__":
    asyncio.run(main())
