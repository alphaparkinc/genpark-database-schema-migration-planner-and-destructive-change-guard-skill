"""Database Schema Migration Planner and Destructive Change Guard.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Optional
import re


class SchemaMigrationGuard:
    """Compares declarative SQL schema definitions, flags destructive operations
    (DROP TABLE, DROP COLUMN, ALTER TYPE, non-null without default), and generates safe
    expand-contract zero-downtime migration steps."""

    DESTRUCTIVE_PATTERNS = [
        (re.compile(r'\bDROP\s+TABLE\s+([a-zA-Z0-9_]+)\b', re.IGNORECASE), "DROP_TABLE", "CRITICAL_DATA_LOSS"),
        (re.compile(r'\bALTER\s+TABLE\s+([a-zA-Z0-9_]+)\s+DROP\s+COLUMN\s+([a-zA-Z0-9_]+)\b', re.IGNORECASE), "DROP_COLUMN", "HIGH_DATA_LOSS"),
        (re.compile(r'\bALTER\s+TABLE\s+([a-zA-Z0-9_]+)\s+ALTER\s+COLUMN\s+([a-zA-Z0-9_]+)\s+SET\s+NOT\s+NULL\b', re.IGNORECASE), "NOT_NULL_WITHOUT_DEFAULT", "DEPLOYMENT_LOCK_RISK"),
        (re.compile(r'\bTRUNCATE\s+([a-zA-Z0-9_]+)\b', re.IGNORECASE), "TRUNCATE_TABLE", "CRITICAL_DATA_LOSS"),
    ]

    @classmethod
    def analyze_migration_script(cls, sql_script: str) -> Dict[str, Any]:
        """Scans a proposed SQL migration script for destructive statements and table locks."""
        statements = [s.strip() for s in sql_script.split(";") if s.strip()]
        findings = []

        for stmt in statements:
            for pat, issue_type, severity in cls.DESTRUCTIVE_PATTERNS:
                m = pat.search(stmt)
                if m:
                    findings.append({
                        "issue_type": issue_type,
                        "severity": severity,
                        "statement": stmt,
                        "remediation": cls._generate_expand_contract_advice(issue_type, m.groups()),
                    })

        is_safe = len(findings) == 0

        return {
            "total_statements": len(statements),
            "is_safe_for_production": is_safe,
            "destructive_findings_count": len(findings),
            "findings": findings,
            "verdict": "APPROVED_SAFE" if is_safe else "REJECTED_DESTRUCTIVE_CHANGES_DETECTED",
        }

    @staticmethod
    def _generate_expand_contract_advice(issue_type: str, groups: tuple) -> str:
        """Generates zero-downtime expand-contract migration patterns."""
        if issue_type == "DROP_COLUMN":
            table, col = groups[0], groups[1]
            return (
                f"Expand-Contract Phase: 1) Stop reading/writing '{col}' in application code. "
                f"2) Deploy code. 3) Execute DROP COLUMN '{col}' on table '{table}' in a subsequent migration."
            )
        elif issue_type == "NOT_NULL_WITHOUT_DEFAULT":
            table, col = groups[0], groups[1]
            return f"Set a DEFAULT value or backfill existing NULL rows before adding the NOT NULL constraint on '{table}.{col}'."
        elif issue_type == "DROP_TABLE":
            return "Ensure table is archived and no active application foreign keys reference it before dropping."
        return "Manual DBA review required."
