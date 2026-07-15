"""Repository quality checks used locally and in CI."""
from __future__ import annotations
import re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LINK=re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
SECRET=re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|client_secret\s*[:=]",re.I)
def main()->int:
    missing=[]
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts or "generated" in path.parts: continue
        for target in LINK.findall(path.read_text(encoding="utf-8")):
            if not target.startswith(("http://","https://","mailto:")) and not (path.parent/target).exists(): missing.append(f"{path.relative_to(ROOT)} -> {target}")
    tracked=subprocess.check_output(["git","ls-files"],cwd=ROOT,text=True).splitlines();secrets=[]
    for name in tracked:
        path=ROOT/name
        if path.is_file():
            try:text=path.read_text(encoding="utf-8")
            except UnicodeDecodeError:continue
            if SECRET.search(text):secrets.append(name)
    if missing: print("Broken links:\n"+"\n".join(missing))
    if secrets: print("Potential secrets:\n"+"\n".join(secrets))
    if missing or secrets:return 1
    print(f"QUALITY PASS: {len(tracked)} tracked files; Markdown links and secret patterns clean")
    return 0
if __name__=="__main__":raise SystemExit(main())
