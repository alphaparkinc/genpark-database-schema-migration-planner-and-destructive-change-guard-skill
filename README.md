# genpark-database-schema-migration-planner-and-destructive-change-guard-skill

Declarative schema diff comparator, destructive SQL operation detector, and zero-downtime migration planner.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **Destructive SQL Operation Guard**: Identifies catastrophic changes (`DROP TABLE`, `DROP COLUMN`, `TRUNCATE`) in database DDL scripts.
- **Table Lock & Constraint Risk Detection**: Flags `SET NOT NULL` statements without defaults that could cause full table locks or migration failures on large production databases.
- **Expand-Contract Remediation Planner**: Recommends multi-phase zero-downtime deployment patterns to safely phase out obsolete columns.

## Architecture

```
[Candidate SQL DDL Migration Script]
                 │
                 ▼
┌──────────────────────────────────────────────────┐
│              SchemaMigrationGuard                │
│  - SQL Tokenizer & Destructive Pattern Regex     │
│  - Table-Lock Risk Classifier                    │
│  - Expand-Contract Zero-Downtime Rule Generator  │
└──────────────────────────────────────────────────┘
                 │
                 ▼
[Production Safety Verdict (APPROVED / REJECTED) + Safe Steps]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `analyze_sql_migration`: Scans SQL migration script for destructive table drops, column deletions, and table lock risks.

## Quickstart (Python API)

```python
from client import SchemaMigrationGuard

sql = "ALTER TABLE users DROP COLUMN phone;"
res = SchemaMigrationGuard.analyze_migration_script(sql)
print(res["verdict"], res["is_safe_for_production"])
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
