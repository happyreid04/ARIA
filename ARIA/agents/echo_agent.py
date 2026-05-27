from agents.base_agent import BaseAgent
from message import AgentMessage
class EchoAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="EchoAgent")
    async def run(self, message: AgentMessage) -> AgentMessage:
        self.log(f"Received message: '{message.task}' from {message.sender}")
        result = {
            "echo": message.payload,
            "note": "EchoAgent received and processed this"
        }
        self.log(f"Task complete - returning result")
        return message.succeed(result)
