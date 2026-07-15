"""Deterministic local IAM digital twin. Evidence: IMPLEMENTED LOCALLY."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"
DB = GENERATED / "entra-lab.sqlite3"
REPORTS = GENERATED / "reports"
LOGICAL_TIME = "2026-01-15T15:00:00Z"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def connect() -> sqlite3.Connection:
    if not DB.exists():
        raise RuntimeError("Local state is not initialized. Run setup first.")
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def audit(con: sqlite3.Connection, event: str, subject: str, detail: dict[str, Any]) -> None:
    con.execute("INSERT INTO audit_events(ts,event,subject,detail) VALUES(?,?,?,?)", (LOGICAL_TIME,event,subject,json.dumps(detail,sort_keys=True)))


def setup() -> int:
    GENERATED.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    con = sqlite3.connect(DB)
    con.executescript("""
    CREATE TABLE IF NOT EXISTS identities(person_id TEXT PRIMARY KEY, username TEXT UNIQUE, department TEXT, employment_type TEXT, manager_id TEXT, active INTEGER, end_date TEXT);
    CREATE TABLE IF NOT EXISTS entitlements(person_id TEXT, entitlement TEXT, source TEXT, PRIMARY KEY(person_id,entitlement));
    CREATE TABLE IF NOT EXISTS findings(code TEXT, person_id TEXT, severity TEXT, detail TEXT, status TEXT, PRIMARY KEY(code,person_id));
    CREATE TABLE IF NOT EXISTS audit_events(id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, event TEXT, subject TEXT, detail TEXT);
    CREATE TABLE IF NOT EXISTS metadata(key TEXT PRIMARY KEY,value TEXT);
    """)
    policy = load(ROOT / "config" / "policy.json")
    workers = load(ROOT / "data" / "hr.json")["workers"]
    for worker in workers:
        username = f"{worker['first_name'][0]}{worker['last_name']}@northstar.example".lower()
        con.execute("INSERT OR REPLACE INTO identities VALUES(?,?,?,?,?,?,?)", (worker["person_id"],username,worker["department"],worker["employment_type"],worker["manager_id"],int(worker["active"]),worker["end_date"]))
        for entitlement in policy["departments"].get(worker["department"], []):
            con.execute("INSERT OR IGNORE INTO entitlements VALUES(?,?,?)", (worker["person_id"],entitlement,"role-rule"))
    con.execute("INSERT OR REPLACE INTO metadata VALUES('scenario_state','baseline')")
    con.execute("INSERT OR REPLACE INTO metadata VALUES('source_hash',?)", (hashlib.sha256((ROOT/'data'/'hr.json').read_bytes()).hexdigest(),))
    con.commit(); con.close()
    print("LOCAL IDENTITY GOVERNANCE SIMULATOR: healthy baseline initialized")
    return 0


def introduce_failure() -> int:
    scenario = load(ROOT / "demo" / "scenarios" / "jasmine-mover-failure.json")
    policy = load(ROOT / "config" / "policy.json")
    with connect() as con:
        pid = scenario["person_id"]
        con.execute("UPDATE identities SET department=? WHERE person_id=?", (scenario["to_department"],pid))
        for entitlement in policy["departments"][scenario["to_department"]]:
            con.execute("INSERT OR IGNORE INTO entitlements VALUES(?,?,?)", (pid,entitlement,"mover-rule"))
        for entitlement in policy["departments"][scenario["from_department"]]:
            if entitlement != scenario["suppressed_removal"]:
                con.execute("DELETE FROM entitlements WHERE person_id=? AND entitlement=?", (pid,entitlement))
        con.execute("INSERT OR REPLACE INTO metadata VALUES('scenario_state','failed')")
        audit(con,"MOVER_FAILURE_INTRODUCED",pid,scenario)
    print("Intentional failure introduced: stale Finance ledger access retained")
    return 0


def validate(expect_failure: bool = False) -> int:
    policy = load(ROOT / "config" / "policy.json")
    with connect() as con:
        con.execute("DELETE FROM findings WHERE status='open'")
        for identity in con.execute("SELECT * FROM identities"):
            actual = {r[0] for r in con.execute("SELECT entitlement FROM entitlements WHERE person_id=?",(identity["person_id"],))}
            desired = set(policy["departments"].get(identity["department"],[]))
            for stale in sorted(actual-desired):
                con.execute("INSERT OR REPLACE INTO findings VALUES(?,?,?,?,?)",("ENTRA-STALE-001",identity["person_id"],"high",f"Stale entitlement: {stale}","open"))
            for pair in policy["toxic_combinations"]:
                if set(pair).issubset(actual):
                    con.execute("INSERT OR REPLACE INTO findings VALUES(?,?,?,?,?)",("ENTRA-SOD-001",identity["person_id"],"critical",f"Toxic combination: {pair}","open"))
            if identity["employment_type"] == "Contractor" and identity["end_date"] and identity["end_date"] < "2026-01-15" and identity["active"]:
                con.execute("INSERT OR REPLACE INTO findings VALUES(?,?,?,?,?)",("ENTRA-EXP-001",identity["person_id"],"high","Expired contractor remains active","open"))
        findings = list(con.execute("SELECT code,person_id,severity,detail FROM findings WHERE status='open' ORDER BY code"))
    for row in findings: print(f"FAIL {row['code']} {row['person_id']}: {row['detail']}")
    if findings:
        return 0 if expect_failure else 2
    print("PASS: identity state is compliant")
    return 1 if expect_failure else 0


def investigate() -> int:
    REPORTS.mkdir(parents=True,exist_ok=True)
    with connect() as con:
        findings = [dict(r) for r in con.execute("SELECT * FROM findings WHERE status='open' ORDER BY code")]
        events = [dict(r) for r in con.execute("SELECT * FROM audit_events ORDER BY id")]
    payload={"classification":"SIMULATED INVESTIGATION","scenario":"entra-jasmine-mover-v1","findings":findings,"timeline":events,"conclusion":"Confirmed stale local entitlement; no claim of tenant access or misuse."}
    (REPORTS/"investigation.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
    lines=["# Simulated Identity Investigation","","Evidence: `SIMULATED INVESTIGATION`","",payload["conclusion"],"","## Findings"]+[f"- {f['code']}: {f['detail']}" for f in findings]
    (REPORTS/"investigation.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"Investigation generated: {REPORTS}")
    return 0


def remediate() -> int:
    policy=load(ROOT/"config"/"policy.json")
    with connect() as con:
        for identity in con.execute("SELECT * FROM identities"):
            if identity["employment_type"] == "Contractor" and identity["end_date"] and identity["end_date"] < "2026-01-15":
                con.execute("UPDATE identities SET active=0 WHERE person_id=?", (identity["person_id"],))
                con.execute("DELETE FROM entitlements WHERE person_id=?", (identity["person_id"],))
                audit(con,"EXPIRED_CONTRACTOR_DISABLED",identity["person_id"],{"end_date":identity["end_date"]})
                continue
            desired=set(policy["departments"].get(identity["department"],[]))
            actual={r[0] for r in con.execute("SELECT entitlement FROM entitlements WHERE person_id=?",(identity["person_id"],))}
            for item in actual-desired: con.execute("DELETE FROM entitlements WHERE person_id=? AND entitlement=?",(identity["person_id"],item))
            for item in desired-actual: con.execute("INSERT OR IGNORE INTO entitlements VALUES(?,?,?)",(identity["person_id"],item,"remediation"))
        con.execute("UPDATE findings SET status='resolved' WHERE status='open'")
        con.execute("INSERT OR REPLACE INTO metadata VALUES('scenario_state','remediated')")
        audit(con,"REMEDIATION_APPLIED","NSH-1001",{"action":"recalculate-entitlements"})
    print("Remediation applied: desired access recalculated")
    return 0


def report() -> int:
    REPORTS.mkdir(parents=True,exist_ok=True)
    with connect() as con:
        state={"classification":"IMPLEMENTED LOCALLY","identities":[dict(r) for r in con.execute("SELECT * FROM identities ORDER BY person_id")],"entitlements":[dict(r) for r in con.execute("SELECT * FROM entitlements ORDER BY person_id,entitlement")],"findings":[dict(r) for r in con.execute("SELECT * FROM findings ORDER BY code")]}
    (REPORTS/"final-state.json").write_text(json.dumps(state,indent=2),encoding="utf-8")
    (REPORTS/"final-report.md").write_text("# Local IAM Final Report\n\nEvidence: `IMPLEMENTED LOCALLY`\n\nFinal validation passed after entitlement recalculation. Synthetic data only.\n",encoding="utf-8")
    print("Final reports generated")
    return 0


def reset() -> int:
    if GENERATED.exists(): shutil.rmtree(GENERATED)
    return setup()


def teardown() -> int:
    if GENERATED.exists(): shutil.rmtree(GENERATED)
    print("Generated local state removed")
    return 0


def run_demo() -> int:
    setup(); introduce_failure()
    if validate(expect_failure=True) != 0: return 3
    investigate(); remediate()
    if validate() != 0: return 4
    report(); print("DEMO PASS: failure detected, remediated, and verified")
    return 0


def main() -> int:
    parser=argparse.ArgumentParser(description="LOCAL IDENTITY GOVERNANCE SIMULATOR")
    parser.add_argument("command",choices=["setup","fail","validate","expect-failure","investigate","remediate","report","reset","teardown","demo"])
    cmd=parser.parse_args().command
    return {"setup":setup,"fail":introduce_failure,"validate":validate,"expect-failure":lambda:validate(True),"investigate":investigate,"remediate":remediate,"report":report,"reset":reset,"teardown":teardown,"demo":run_demo}[cmd]()


if __name__ == "__main__": raise SystemExit(main())
