"""Configuration-as-data validators for Entra-aligned controls."""
from __future__ import annotations
import argparse,json
from datetime import date
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
def read(path:Path)->dict[str,Any]: return json.loads(path.read_text(encoding="utf-8"))
def validate_ca(doc:dict[str,Any])->list[dict[str,str]]:
    findings=[]; policies=doc.get("policies",[]); emergency=set(doc.get("emergency_accounts",[]))
    if len(doc.get("trusted_locations",[]))>2: findings.append({"code":"CA-LOC-001","severity":"high","detail":"Excessive trusted locations"})
    if not any("Guest" in p.get("include_user_types",[]) for p in policies): findings.append({"code":"CA-GUEST-001","severity":"high","detail":"Guests are not explicitly protected"})
    if not any(p.get("include_roles") and "mfa" in p.get("grant",[]) for p in policies): findings.append({"code":"CA-ADMIN-001","severity":"critical","detail":"Privileged roles lack explicit MFA policy"})
    for p in policies:
        excluded=set(p.get("exclude_users",[]))
        if emergency and not emergency.issubset(excluded): findings.append({"code":"CA-BG-001","severity":"critical","detail":f"{p['name']} lacks emergency exclusion"})
        if len(excluded-emergency)>1: findings.append({"code":"CA-EXCL-001","severity":"high","detail":f"{p['name']} has broad exclusions"})
        if p.get("legacy_auth")!="blocked": findings.append({"code":"CA-LEGACY-001","severity":"critical","detail":f"{p['name']} allows legacy authentication"})
        if "mfa" not in p.get("grant",[]): findings.append({"code":"CA-MFA-001","severity":"critical","detail":f"{p['name']} does not require MFA"})
        if p.get("state")!="reportOnly": findings.append({"code":"CA-STAGE-001","severity":"medium","detail":f"{p['name']} has no report-only stage"})
    return findings
def validate_apps(doc:dict[str,Any])->list[dict[str,str]]:
    findings=[]; risky=set(doc.get("high_risk_permissions",[])); today=date(2026,1,15)
    for app in doc.get("applications",[]):
        if not app.get("owners"): findings.append({"code":"APP-OWNER-001","severity":"high","detail":f"{app['name']} has no owner"})
        if risky.intersection(app.get("permissions",[])): findings.append({"code":"APP-PERM-001","severity":"critical","detail":f"{app['name']} has excessive application permission"})
        if date.fromisoformat(app["credential_expires"])<today: findings.append({"code":"APP-CRED-001","severity":"high","detail":f"{app['name']} credential is expired"})
        if app.get("credential_type")=="secret": findings.append({"code":"APP-SECRET-001","severity":"medium","detail":f"{app['name']} should migrate from secret to certificate"})
        if not app.get("assignment_required"): findings.append({"code":"APP-ASSIGN-001","severity":"medium","detail":f"{app['name']} does not require assignment"})
    return findings
def validate_governance(doc:dict[str,Any])->list[dict[str,str]]:
    findings=[]; privilege=doc.get("privilege",{}); guest=doc.get("guest",{})
    if privilege.get("default_assignment")!="eligible": findings.append({"code":"GOV-PIM-001","severity":"critical","detail":"Privilege is not eligible by default"})
    if privilege.get("permanent_assignments_allowed"): findings.append({"code":"GOV-PIM-002","severity":"high","detail":"Permanent privilege is allowed"})
    if not guest.get("sponsor_required") or not guest.get("renewal_required"): findings.append({"code":"GOV-GUEST-001","severity":"high","detail":"Guest sponsorship or renewal control missing"})
    for package in doc.get("access_packages",[]):
        if not package.get("justification_required") or not package.get("review_frequency_days"): findings.append({"code":"GOV-PKG-001","severity":"high","detail":f"{package['name']} lacks justification or review"})
    return findings
def report(kind:str,path:Path)->int:
    doc=read(path); fn={"ca":validate_ca,"apps":validate_apps,"governance":validate_governance}[kind]; findings=fn(doc)
    out=ROOT/"generated"/"reports";out.mkdir(parents=True,exist_ok=True)
    payload={"classification":"IMPLEMENTED LOCALLY","validator":kind,"source_classification":doc.get("classification"),"findings":findings,"status":"fail" if findings else "pass"}
    (out/f"{kind}-validation.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
    print(json.dumps(payload,indent=2));return 2 if findings else 0
def main()->int:
    p=argparse.ArgumentParser();p.add_argument("kind",choices=["ca","apps","governance"]);p.add_argument("path",type=Path);a=p.parse_args();return report(a.kind,a.path)
if __name__=="__main__":raise SystemExit(main())
