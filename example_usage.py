"""Example usage for Database Schema Migration Planner & Destructive Change Guard."""
from client import SchemaMigrationGuard

if __name__ == "__main__":
    risky_sql = """
    ALTER TABLE users ADD COLUMN age INT;
    ALTER TABLE users DROP COLUMN legacy_auth_token;
    ALTER TABLE orders ALTER COLUMN status SET NOT NULL;
    """

    res = SchemaMigrationGuard.analyze_migration_script(risky_sql)
    print("Migration Safe for Production:", res["is_safe_for_production"])
    print("Verdict:", res["verdict"])
    for f in res["findings"]:
        print(f"\n[{f['severity']}] {f['issue_type']}: {f['statement']}")
        print("  Remediation:", f["remediation"])
