#!/usr/bin/env python3
"""Parse the Central Asia AI Education Audit 2026 markdown tables into CSV + JSON.
Source: ~/workspace/aclas-kg-seo/research/central-asia-ai-education-audit-2026.md
Run: python3 parse.py
"""
import csv, json, re
from pathlib import Path

SRC = Path.home() / "workspace/aclas-kg-seo/research/central-asia-ai-education-audit-2026.md"
OUT = Path(__file__).parent

def split_row(line: str):
    parts = re.split(r'(?<!\\)\|', line.strip())
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [p.replace("\\|", "|").strip() for p in parts]

def is_header_or_sep(cells):
    if not cells:
        return True
    first = cells[0].strip()
    if re.fullmatch(r"[\s\-|:]+", first):
        return True
    return not re.match(r"^[\d]", first)

def first_url(text):
    if not text:
        return None
    m = re.search(r"https?://\S+", text)
    return m.group(0).rstrip(").,;") if m else None

def norm_policy(v):
    v = re.sub(r"\*", "", v).strip().upper()
    if v.startswith("YES"):
        return "YES"
    if v.startswith("NO"):
        return "NO"
    return "UNVERIFIABLE"

lines = SRC.read_text(encoding="utf-8").splitlines()
# locate the two tables
t1_start = next(i for i, l in enumerate(lines) if l.startswith("| # | Country | University | AI policy |"))
t2_start = next(i for i, l in enumerate(lines) if l.startswith("| # | University | AI programs"))

def parse_table(start):
    rows = []
    for line in lines[start:]:
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = split_row(line)
        if is_header_or_sep(cells):
            continue
        rows.append(cells)
    return rows

policies, programs = [], []
for cells in parse_table(t1_start):
    url_raw = cells[4]
    policies.append({
        "id": f"ca-{cells[0]}",
        "country_code": cells[1],
        "university": cells[2],
        "has_policy": norm_policy(cells[3]),
        "policy_url": first_url(url_raw),
        "policy_url_raw": url_raw if url_raw not in ("—", "-", "") and url_raw != first_url(url_raw) else None,
        "note": cells[5] or None,
    })
for cells in parse_table(t2_start):
    url_raw = cells[3] if len(cells) > 3 else ""
    programs.append({
        "id": f"ca-p-{cells[0]}",
        "university": cells[1],
        "ai_programs": cells[2] or None,
        "source_url": first_url(url_raw),
        "source_url_raw": url_raw if url_raw not in ("—", "-", "") and url_raw != first_url(url_raw) else None,
    })

print(f"policy rows: {len(policies)}")
print(f"program rows: {len(programs)}")
from collections import Counter
print("policy counts:", dict(Counter(p["has_policy"] for p in policies)))

for name, rows, fields in [
    ("central-asia-ai-policies-2026", policies,
     ["id", "country_code", "university", "has_policy", "policy_url", "policy_url_raw", "note"]),
    ("central-asia-ai-programs-2026", programs,
     ["id", "university", "ai_programs", "source_url", "source_url_raw"]),
]:
    with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print("wrote", name)

with open(OUT / "central-asia-ai-education-audit-2026.json", "w", encoding="utf-8") as f:
    json.dump({
        "dataset": "Central Asia AI Education Audit 2026",
        "audit_date": "2026-10-17",
        "publisher": "Study Intelligence (aclas.si)",
        "license": "CC-BY-4.0",
        "ai_policies": policies,
        "ai_programs": programs,
    }, f, ensure_ascii=False, indent=2)
print("wrote json")
