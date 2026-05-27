from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
@dataclass
class AgentMessage:
    task: str
    payload: dict
    sender: str
    receiver: str
    status: str = "pending"
    result: Any = None
    error: str = None
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    def succeed(self, result: Any) -> "AgentMessage":
        """Agent calls this when it successfully"""
        self.status = "success"
        self.result = result
        return self
    def fail(self, error: str) -> "AgentMessage":
        """Agent calls this when it fails"""
        self.status = "failed"
        self.error = error
        return self
    def forward(self, new_receiver: str) -> "AgentMessage":
        """Pass this message to the next agent"""
        self.sender = self.receiver
        self.receiver = self.receiver 
        return self
    
