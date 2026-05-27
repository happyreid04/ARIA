import asyncio
from message import AgentMessage
from agents.echo_agent import EchoAgent
async def main():
    msg = AgentMessage(
        task="test communication",
        payload={"query": "Does the communication between agents work?"},
        sender="human",
        receiver="EchoAgent"
    )
    agent = EchoAgent()
    result = await agent.run(msg)
    print(f"\nStatus: {result.status}")
    print(f"Result: {result.result}")
    print(f"Timestamp: {result.timestamp}")
if __name__ == "__main__":
    asyncio.run(main())

