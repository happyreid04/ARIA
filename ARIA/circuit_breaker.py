from enum import Enum
from datetime import datetime, timedelta
class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"
class CircuitBreaker:
    def __init__(
            self,
            agent_name: str,
            failure_threshold: int = 3,
            recovery_timeout: int = 60,
    ):
        self.agent_name = agent_name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
    def record_success(self):
        """Agent succeeded - reset everything"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            print(f"[CircuitBreaker] {self.agent_name} circuit OPENED after {self.failure_count} failures")
    def can_proceed(self) -> bool:
        """
        Check if requests should go through.
        CLOSED  - yes always
        OPEN    - check if recovery timeout passed, maybe try again
        HALF_OPEN = one test request allowed
        """
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            if datetime.now() - self.last_failure_time > timedelta(second=self.recovery_timeout):
               self.state = CircuitState.HALF_OPEN
               print(f"[CircuitBreaker] {self.agent_name} circuit HALF_OPEN - testing recovery")
               return True
            return False
        if self.state == CircuitState.HALF_OPEN:
            return True
        return False
    