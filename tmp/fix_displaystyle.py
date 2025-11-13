import re
from pathlib import Path

path = Path(r"c:\Users\SWEELCO-AT\Desktop\SWINDER\OptiTABV2\frontend\cours\cours_optitab\cours_arithmetique_entiers_mpsi.txt")
text = path.read_text(encoding="utf-8")

# Remove existing \displaystyle tokens to start from a clean slate.
text = text.replace("\\displaystyle", "")

pattern = re.compile(r"\$(.*?)\$", re.DOTALL)

def ensure_displaystyle(match: re.Match) -> str:
    content = match.group(1)
    stripped = content.strip()
    if stripped.startswith("\\displaystyle"):
        return f"${stripped}$"
    return f"$\\displaystyle {stripped}$"

text = pattern.sub(ensure_displaystyle, text)
path.write_text(text, encoding="utf-8")
