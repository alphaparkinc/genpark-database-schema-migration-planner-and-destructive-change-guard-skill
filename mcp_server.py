"""MCP server for Database Schema Migration Planner & Destructive Change Guard."""
import sys
import json
from client import SchemaMigrationGuard


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "analyze_sql_migration",
                    "description": "Scans SQL migration script for destructive table drops, column deletions, and table lock risks",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "sql_script": {"type": "string"},
                        },
                        "required": ["sql_script"],
                    },
                }
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "analyze_sql_migration":
            res = SchemaMigrationGuard.analyze_migration_script(args.get("sql_script", ""))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
