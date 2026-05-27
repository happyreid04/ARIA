from message import AgentMessage
class BaseAgent:
    def __init__(self, name: str):
        self.name = name
    async def run(self, message: AgentMessage) -> AgentMessage:
        """Override this method to implement the agent's logic"""
        raise NotImplementedError(f"{self.name} must implement run()")
    def log(self, text: str):
        """Simple logging method"""
        print(f"[{self.name}] {text}")
        
