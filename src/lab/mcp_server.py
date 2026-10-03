"""Limited MCP 2025-11-25 stdio adapter for two read-only synthetic tools."""
import json
import sys
from .controller import Lab, load_data

VERSION = "2025-11-25"
TOOLS = [
    {"name": "lookup_demo_order", "description": "Read a synthetic order in the sample workspace.",
     "inputSchema": {"type": "object", "properties": {"order_id": {"type": "string"}},
                     "required": ["order_id"], "additionalProperties": False},
     "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False}},
    {"name": "read_demo_policy", "description": "Read the fictional exercise policy.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
     "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False}}
]

class Protocol:
    def __init__(self):
        self.initialized = False
        self.ready = False
        self.lab = Lab()

    def handle(self, message):
        request_id = message.get("id") if isinstance(message, dict) else None
        def error(code, text):
            return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": text}}
        if not isinstance(message, dict) or message.get("jsonrpc") != "2.0" or not isinstance(message.get("method"), str):
            return error(-32600, "Invalid request")
        method = message["method"]
        params = message.get("params", {})
        if not isinstance(params, dict):
            return error(-32602, "Invalid params") if "id" in message else None
        if "id" not in message:
            if method == "notifications/initialized" and self.initialized:
                self.ready = True
            return None
        if method == "initialize":
            if self.initialized:
                return error(-32600, "Already initialized")
            if not isinstance(params.get("protocolVersion"), str) or not isinstance(params.get("capabilities"), dict):
                return error(-32602, "Initialization fields required")
            info = params.get("clientInfo")
            if not isinstance(info, dict) or not isinstance(info.get("name"), str) or not isinstance(info.get("version"), str):
                return error(-32602, "Client information required")
            self.initialized = True
            result = {"protocolVersion": VERSION, "serverInfo": {"name": "implementation-lab", "version": "0.1.0"},
                      "capabilities": {"tools": {"listChanged": False}}}
        elif method == "ping":
            result = {}
        elif not self.ready:
            return error(-32002, "Initialize first")
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            name = params.get("name")
            args = params.get("arguments", {})
            if not isinstance(args, dict):
                return error(-32602, "Invalid arguments")
            if name == "read_demo_policy" and not args:
                payload = load_data("policy.json")
            elif name == "lookup_demo_order" and set(args) == {"order_id"} and isinstance(args["order_id"], str):
                payload = self.lab.request({"intent": "lookup", "order_id": args["order_id"]})
            else:
                return error(-32602, "Unknown tool or invalid arguments")
            result = {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=True)}],
                      "isError": payload.get("status") == "BLOCKED"}
        else:
            return error(-32601, "Method not found")
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

def serve():
    protocol = Protocol()
    for line in sys.stdin:
        if len(line) > 16384:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Message too large"}}
        else:
            try:
                response = protocol.handle(json.loads(line))
            except (ValueError, TypeError):
                response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
        if response is not None:
            print(json.dumps(response, ensure_ascii=True), flush=True)
