"""Application lifecycle hooks, invoked by the controller, not assistant permissions."""
import hashlib
import json

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

class AuditTrail:
    def __init__(self):
        self.events = []

    def append(self, phase, action, outcome, reference=""):
        event = {"sequence": len(self.events) + 1, "phase": phase, "action": action,
                 "outcome": outcome, "reference": reference,
                 "previous": self.events[-1]["hash"] if self.events else "GENESIS"}
        event["hash"] = digest(event)
        self.events.append(event)
        return event

    @staticmethod
    def verify(events):
        previous = "GENESIS"
        for index, original in enumerate(events, 1):
            event = dict(original)
            signature = event.pop("hash", None)
            if event.get("sequence") != index or event.get("previous") != previous:
                return False
            if digest(event) != signature:
                return False
            previous = signature
        return True
