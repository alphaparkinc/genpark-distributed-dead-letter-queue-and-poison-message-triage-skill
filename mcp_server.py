"""MCP server for Dead Letter Queue Triager."""
import sys
import json
from client import DeadLetterQueueTriager

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "triage_dlq_message",
                "description": "Classifies failed DLQ message reasons and assigns retry delays or quarantine",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "error_reason": {"type": "string"},
                        "attempts": {"type": "integer"},
                        "max_attempts": {"type": "integer"}
                    },
                    "required": ["error_reason", "attempts"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "triage_dlq_message":
            args = params.get("arguments", {})
            res = DeadLetterQueueTriager.triage_dead_letter(
                args.get("error_reason", ""),
                int(args.get("attempts", 1)),
                int(args.get("max_attempts", 3))
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
