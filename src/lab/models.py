"""Small domain objects: data and decisions are separate from tools and views."""
from dataclasses import dataclass, asdict

class RuleError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)

@dataclass
class Proposal:
    id: str
    order_id: str
    amount: int
    order_version: int
    order_digest: str
    policy_digest: str
    status: str = "PENDING_APPROVAL"

    def as_dict(self):
        return asdict(self)
