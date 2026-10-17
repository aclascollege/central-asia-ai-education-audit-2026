#!/usr/bin/env python3
"""Parse the 187-university AI policy audit markdown tables into CSV + JSON.
Source: ~/workspace/aclas-report/ai-policy-audit/ (audit date 2026-10-14).
Run: python3 parse.py  (writes ai-policy-audit-2026.csv / .json next to this file)
"""
import csv, json, re, sys
from pathlib import Path

SRC = Path.home() / "workspace/aclas-report/ai-policy-audit"
OUT = Path(__file__).parent

FILES = [
    ("qs-001-050.md", "qs_top_50"),
    ("qs-051-100.md", "qs_51_100"),
    ("qs-101-150.md", "qs_101_150"),
    ("global-south-35.md", "global_south"),
]

def split_row(line: str):
    # split on unescaped pipes; "\|" inside a cell is a literal pipe
    parts = re.split(r'(?<!\\)\|', line.strip())
    # drop leading/trailing empty from outer pipes
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
    # data rows start with a digit (rank) or '=' (tied rank); headers start with '#', 'Rank', 'QS rank', ...
    if not re.match(r"^[=\d]", first):
        return True
    return False

def parse_file(fname, sample):
    rows = []
    for line in (SRC / fname).read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = split_row(line)
        if is_header_or_sep(cells):
            continue
        rows.append((sample, cells))
    return rows

def norm_policy(v):
    v = v.strip().upper()
    if v.startswith("YES"):
        return "YES"
    if v.startswith("NO"):
        return "NO"
    return "UNCLEAR"

records, warnings = [], []
for fname, sample in FILES:
    for _, cells in parse_file(fname, sample):
        try:
            if sample == "global_south":
                # # | University | Country | Has Policy | Policy page URL | Title | Date | Scope | Note
                rec = {
                    "id": f"gs-{cells[0]}",
                    "sample": sample,
                    "rank": None,
                    "university": cells[1],
                    "country": cells[2] or None,
                    "official_domain": None,
                    "has_policy": norm_policy(cells[3]),
                    "policy_url": cells[4] if cells[4] not in ("—", "-", "") else None,
                    "page_title": cells[5] or None,
                    "date_info": cells[6] or None,
                    "scope": cells[7] or None,
                    "note": cells[8] or None,
                }
            elif sample == "qs_51_100":
                # # | University | QS 2026 | Policy? | Policy page URL | Page title | Date | Scope | Note
                rec = {
                    "id": f"qs-{cells[2].lstrip('=')}",
                    "sample": sample,
                    "rank": cells[2],
                    "university": cells[1],
                    "country": None,
                    "official_domain": None,
                    "has_policy": norm_policy(cells[3]),
                    "policy_url": cells[4] if cells[4] not in ("—", "-", "") else None,
                    "page_title": cells[5] or None,
                    "date_info": cells[6] or None,
                    "scope": cells[7] or None,
                    "note": cells[8] or None,
                }
            elif sample == "qs_101_150":
                # QS rank | University | HAS POLICY | Policy page URL | Page title / date | Scope | One-line note
                # (no official-domain column; page_title and date are combined)
                rec = {
                    "id": f"qs-{cells[0].lstrip('=')}",
                    "sample": sample,
                    "rank": cells[0],
                    "university": cells[1],
                    "country": None,
                    "official_domain": None,
                    "has_policy": norm_policy(cells[2]),
                    "policy_url": cells[3] if cells[3] not in ("—", "-", "") else None,
                    "page_title": cells[4] or None,
                    "date_info": None,
                    "scope": cells[5] or None,
                    "note": cells[6] or None,
                }
            else:
                # Rank | University | Official domain | HAS POLICY | Policy page URL | Page title | Date | Scope | One-line note
                rec = {
                    "id": f"qs-{cells[0].lstrip('=')}",
                    "sample": sample,
                    "rank": cells[0],
                    "university": cells[1],
                    "country": None,
                    "official_domain": cells[2] or None,
                    "has_policy": norm_policy(cells[3]),
                    "policy_url": cells[4] if cells[4] not in ("—", "-", "") else None,
                    "page_title": cells[5] or None,
                    "date_info": cells[6] or None,
                    "scope": cells[7] or None,
                    "note": cells[8] or None,
                }
        except IndexError:
            warnings.append(f"{fname}: short row skipped: {cells[:3]}")
            continue
        records.append(rec)

# ---- post-processing ----
import re as _re
def _first_url(text):
    if not text:
        return None
    m = _re.search(r"https?://\S+", text)
    return m.group(0).rstrip(").,;") if m else None

seen_ids = {}
for rec in records:
    raw = rec.get("policy_url")
    clean = _first_url(raw)
    rec["policy_url_raw"] = raw if (raw and raw != clean) else None
    rec["policy_url"] = clean
    base = rec["id"]
    if base in seen_ids:
        seen_ids[base] += 1
        rec["id"] = f"{base}-{seen_ids[base]}"
    else:
        seen_ids[base] = 1

# name overlap flag (same university audited in more than one sample)
from collections import Counter as _Counter
_name_counts = _Counter(r["university"].strip().lower() for r in records)
for rec in records:
    rec["name_overlap"] = _name_counts[rec["university"].strip().lower()] > 1

# ---- validation ----
from collections import Counter
counts = Counter(r["has_policy"] for r in records)
per_sample = Counter(r["sample"] for r in records)
print(f"total rows: {len(records)}")
print(f"by policy: {dict(counts)}")
print(f"by sample: {dict(per_sample)}")
if warnings:
    print("WARNINGS:")
    [print(" ", w) for w in warnings]

FIELDS = ["id", "sample", "rank", "university", "country", "official_domain",
          "has_policy", "policy_url", "policy_url_raw", "page_title", "date_info",
          "scope", "note", "name_overlap"]
with open(OUT / "ai-policy-audit-2026.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(records)
with open(OUT / "ai-policy-audit-2026.json", "w", encoding="utf-8") as f:
    json.dump({
        "dataset": "Global University AI Policy Audit 2026",
        "audit_date": "2026-10-14",
        "publisher": "Study Intelligence (aclas.si)",
        "license": "CC-BY-4.0",
        "records": records,
    }, f, ensure_ascii=False, indent=2)
print("wrote csv + json")
