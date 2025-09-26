import re
def clean_text(s: str) -> str:
    s = s.replace("\u200b", " ").replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s
