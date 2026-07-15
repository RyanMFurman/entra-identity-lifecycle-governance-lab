from automation.controls import read,validate_apps,validate_ca,validate_governance
from automation.controls import ROOT
def codes(rows): return {r["code"] for r in rows}
def test_safe_ca_passes(): assert validate_ca(read(ROOT/"config/conditional-access/safe.json"))==[]
def test_unsafe_ca_fails_expected_controls():
    found=codes(validate_ca(read(ROOT/"config/conditional-access/unsafe.json")))
    assert {"CA-BG-001","CA-MFA-001","CA-LEGACY-001","CA-STAGE-001","CA-GUEST-001","CA-ADMIN-001"}.issubset(found)
def test_governance_design_passes(): assert validate_governance(read(ROOT/"config/governance.json"))==[]
def test_application_risks_are_detected():
    found=codes(validate_apps(read(ROOT/"config/applications.json")))
    assert {"APP-OWNER-001","APP-PERM-001","APP-CRED-001","APP-SECRET-001","APP-ASSIGN-001"}.issubset(found)
