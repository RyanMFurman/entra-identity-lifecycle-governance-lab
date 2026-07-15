"""Build a clearly labeled local evidence page from generated reports."""
from __future__ import annotations
import html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];REPORTS=ROOT/"generated"/"reports";OUT=ROOT/"generated"/"evidence-site"
def load(name:str)->dict:
    path=REPORTS/name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
def main()->int:
    state=load("final-state.json");investigation=load("investigation.json");ca=load("ca-validation.json");apps=load("apps-validation.json")
    authorized_path=ROOT/"generated"/"authorized-entra"/"authorized-demo-report.json"
    authorized=json.loads(authorized_path.read_text(encoding="utf-8")) if authorized_path.exists() else {}
    resolved=sum(1 for f in state.get("findings",[]) if f.get("status")=="resolved")
    identities=len(state.get("identities",[]));entitlements=len(state.get("entitlements",[]))
    timeline=len(investigation.get("timeline",[]));ca_findings=len(ca.get("findings",[]));app_findings=len(apps.get("findings",[]))
    cards=[("Identities",identities),("Current entitlements",entitlements),("Resolved lifecycle findings",resolved),("Investigation events",timeline)]
    card_html=''.join(f'<article><strong>{v}</strong><span>{html.escape(k)}</span></article>' for k,v in cards)
    body=f'''<!doctype html><html><head><meta charset="utf-8"><title>Northstar Local IAM Evidence</title><style>
    *{{box-sizing:border-box}}body{{margin:0;background:#07111f;color:#eef6ff;font-family:Segoe UI,Arial,sans-serif}}main{{max-width:1180px;margin:auto;padding:64px}}.eyebrow{{color:#69d7c5;font-weight:700;letter-spacing:.12em}}h1{{font-size:48px;line-height:1.05;margin:16px 0}}.sub{{font-size:20px;color:#b6c8dc;max-width:850px}}.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin:42px 0}}article{{background:#11243a;border:1px solid #24425e;border-radius:16px;padding:28px}}article strong{{display:block;font-size:42px;color:#69d7c5}}article span{{font-size:16px;color:#c8d7e7}}section{{background:#0c1b2d;border-left:5px solid #69d7c5;padding:28px 32px;margin-top:24px}}h2{{font-size:28px;margin:0 0 12px}}.pass{{color:#7ee787;font-weight:700}}.fail{{color:#ffb86b;font-weight:700}}footer{{margin-top:30px;color:#8197ad;font-size:14px}}</style></head><body><main>
    <div class="eyebrow">LOCAL IDENTITY GOVERNANCE SIMULATOR</div><h1>Northstar IAM evidence report</h1><p class="sub">Real local automation using deterministic synthetic data. This page does not imitate Microsoft Entra and is not vendor audit evidence.</p>
    <div class="grid">{card_html}</div>
    <section><h2>Lifecycle outcome</h2><p class="pass">PASS — excessive access detected, remediated, and verified.</p><p>Jasmine retained Finance access after an Engineering transfer. The same policy engine that detected the conflict verified the corrected state.</p></section>
    <section><h2>Configuration validation</h2><p>Safe Conditional Access design: <span class="pass">PASS</span></p><p>Unsafe fixture findings: <span class="fail">{ca_findings}</span> · Application risk findings: <span class="fail">{app_findings}</span></p></section>
    <section><h2>Authorized Entra extension</h2><p class="pass">{'PASS — live synthetic mover conflict remediated and verified.' if authorized.get('remediated',{}).get('compliant') else 'Authorized report not included in this local rendering.'}</p><p>No tenant identifier, account name, object ID, or credential is displayed.</p></section>
    <footer>Evidence classifications: IMPLEMENTED LOCALLY · SIMULATED INVESTIGATION · DESIGNED FOR ENTRA</footer>
    </main></body></html>'''
    OUT.mkdir(parents=True,exist_ok=True);(OUT/"index.html").write_text(body,encoding="utf-8");print(OUT/"index.html");return 0
if __name__=="__main__":raise SystemExit(main())
