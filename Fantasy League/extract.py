# extract_data.py
# Reads the live workbook in read-only mode and dumps EVERYTHING we need
# to rebuild it with POINTS HISTORY + dynamic player list.
#
# Safe: opens read-only, never writes to the workbook.
# Run from PowerShell in C:\Users\chine\OneDrive\Python Stuff\Fantasy League\
#   python extract_data.py

import json
import os
import sys
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

# =========================================================
# CONFIG
# =========================================================
WORKBOOK = r"C:\Users\chine\OneDrive\Copies School Fantasy League for editing\11O Fantasy League.xlsx"
OUTPUT_DIR = r"C:\Users\chine\OneDrive\Python Stuff\Fantasy League\extract_output"
SHEETS_SUBDIR = "sheets"

# Key ranges to extract per sheet. (start_row, start_col, end_row, end_col) as 1-based indices.
# Extra sheets not listed here still get a full "used range" blind dump.
KEY_RANGES = {
    "SETTINGS":       [(1, 1, 80, 26)],   # A1:Z80 — covers rules, prices, log, season config
    "MASTER DATA":    [(1, 1, 30, 12)],   # A1:L30
    "TEST RESULTS":   [(1, 1, 35, 12)],   # A1:L35
    "RAW RESULTS":    [(1, 1, 30, 25)],   # A1:Y30
    "CALCULATIONS":   [(1, 1, 30, 30)],   # A1:AD30
    "POINTS HISTORY": [(1, 1, 30, 25)],   # A1:Y30 (may not exist)
    "HOME":           [(1, 1, 45, 12)],   # A1:L45
    "PLAYER MARKET":  [(1, 1, 35, 10)],   # A1:J35
}

# Leaderboards have inconsistent names — script will fuzzy-match these.
LEADERBOARD_MATCHERS = {
    "OVERALL_LEADERBOARD": ["overall leaderboard"],
    "GW_LEADERBOARD":      ["gw leaderboard", "gameweek leaderboard"],
}

# =========================================================
# HELPERS
# =========================================================
def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def col_letter(idx):
    return get_column_letter(idx)

def read_range(ws, r1, c1, r2, c2):
    """Return dict of {'B5': {'v': ..., 'f': ...}} for the given range.
       Value comes from wb_data (cached), formula from wb_formulas."""
    out = {}
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            ref = f"{col_letter(c)}{r}"
            out[ref] = {"v": None, "f": None}
    return out

def dump_ws_range(ws_formula, ws_data, r1, c1, r2, c2):
    """Extract values (cached) and formulas for a rectangular region."""
    cells = {}
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            ref = f"{col_letter(c)}{r}"
            fcell = ws_formula[ref] if ws_formula is not None else None
            dcell = ws_data[ref] if ws_data is not None else None
            val = dcell.value if dcell is not None else None
            frm = fcell.value if fcell is not None else None
            if val is None and frm is None:
                continue
            cells[ref] = {"v": val, "f": frm if isinstance(frm, str) and frm.startswith("=") else None}
    return cells

def dump_used_range(ws_formula, ws_data):
    """Blind dump of ws_formula's used range. Falls back gracefully."""
    if ws_formula is None and ws_data is None:
        return {}
    ref_ws = ws_formula if ws_formula is not None else ws_data
    max_r = ref_ws.max_row or 1
    max_c = ref_ws.max_column or 1
    return dump_ws_range(ws_formula, ws_data, 1, 1, max_r, max_c)

def merge_list(ws):
    return [str(m) for m in ws.merged_cells.ranges]

def dv_list(ws):
    out = []
    for dv in ws.data_validations.dataValidation:
        out.append({
            "type": dv.type,
            "formula1": str(dv.formula1) if dv.formula1 else None,
            "formula2": str(dv.formula2) if dv.formula2 else None,
            "allow_blank": bool(dv.allow_blank),
            "sqref": str(dv.sqref),
        })
    return out

def fuzzy_match_sheet(sheetnames, matchers):
    for name in sheetnames:
        lower = name.lower().strip()
        for m in matchers:
            if m in lower:
                return name
    return None

# =========================================================
# LOAD
# =========================================================
print("=" * 62)
print("FANTASY LEAGUE — DATA EXTRACTION")
print("=" * 62)
print(f"Workbook: {WORKBOOK}")
print(f"Output:   {OUTPUT_DIR}")
print()

if not os.path.exists(WORKBOOK):
    print(f"ERROR: workbook not found at {WORKBOOK}")
    sys.exit(1)

ensure_dir(OUTPUT_DIR)
ensure_dir(os.path.join(OUTPUT_DIR, SHEETS_SUBDIR))

print("Loading workbook (formulas view)...")
wb_f = load_workbook(WORKBOOK, data_only=False, read_only=False)
print("Loading workbook (cached values view)...")
wb_d = load_workbook(WORKBOOK, data_only=True, read_only=False)

sheetnames_f = wb_f.sheetnames
sheetnames_d = wb_d.sheetnames

if set(sheetnames_f) != set(sheetnames_d):
    print("WARNING: formula-view and data-view sheet lists differ!")
    print(f"  formulas: {sheetnames_f}")
    print(f"  data:     {sheetnames_d}")

# =========================================================
# SHEET STATES
# =========================================================
sheet_states = {}
for name in sheetnames_f:
    ws = wb_f[name]
    state = ws.sheet_state  # 'visible' | 'hidden' | 'veryHidden'
    tab = ws.sheet_properties.tabColor
    sheet_states[name] = {
        "state": state,
        "tab_color": str(tab.rgb) if tab and tab.rgb else None,
        "index": sheetnames_f.index(name),
    }

with open(os.path.join(OUTPUT_DIR, "sheet_states.txt"), "w", encoding="utf-8") as fh:
    fh.write(f"Extracted: {datetime.now().isoformat()}\n")
    fh.write(f"Workbook:  {WORKBOOK}\n\n")
    fh.write(f"{'#':<3} {'State':<12} Tab     Sheet Name\n")
    fh.write("-" * 70 + "\n")
    for i, name in enumerate(sheetnames_f):
        info = sheet_states[name]
        tab = info["tab_color"] or ""
        fh.write(f"{i:<3} {info['state']:<12} {tab:<7} {name}\n")

print()
print("Sheet states:")
for name, info in sheet_states.items():
    print(f"  {info['state']:<12} {name}")

# =========================================================
# NAMED RANGES
# =========================================================
named_ranges = {}
for name, dn in wb_f.defined_names.items():
    try:
        named_ranges[name] = {
            "value": dn.value,
            "type":  str(dn.type) if hasattr(dn, "type") else None,
            "localSheetId": getattr(dn, "localSheetId", None),
        }
    except Exception as e:
        named_ranges[name] = {"error": str(e)}

print()
print(f"Named ranges: {len(named_ranges)}")
for n in named_ranges:
    print(f"  {n}")

# =========================================================
# EXTRACT KEY RANGES + BLIND DUMPS
# =========================================================
extracted = {
    "meta": {
        "workbook": WORKBOOK,
        "extracted_at": datetime.now().isoformat(),
        "sheet_order": sheetnames_f,
        "sheet_states": sheet_states,
        "named_ranges": named_ranges,
    },
    "sheets": {},
}

# Figure out the actual names of the leaderboards
overall_name = fuzzy_match_sheet(sheetnames_f, LEADERBOARD_MATCHERS["OVERALL_LEADERBOARD"])
gw_name      = fuzzy_match_sheet(sheetnames_f, LEADERBOARD_MATCHERS["GW_LEADERBOARD"])
print()
print(f"Overall Leaderboard sheet name → {overall_name!r}")
print(f"GW Leaderboard sheet name      → {gw_name!r}")

# Add leaderboards to key ranges dynamically
dynamic_key_ranges = dict(KEY_RANGES)
if overall_name:
    dynamic_key_ranges[overall_name] = [(1, 1, 35, 8)]
if gw_name:
    dynamic_key_ranges[gw_name] = [(1, 1, 35, 8)]

# Team sheets: any sheet that isn't in the known list gets treated as a manager sheet
known_non_team = set(dynamic_key_ranges.keys()) | {
    "SETTINGS", "CALCULATIONS", "MASTER DATA", "RAW RESULTS",
    "POINTS HISTORY", "HOME", "PLAYER MARKET", "RULES",
    "PICK YOUR TEAM", "TEST RESULTS", "_DIAGNOSTICS",
}
if overall_name: known_non_team.add(overall_name)
if gw_name:      known_non_team.add(gw_name)

team_sheets = [s for s in sheetnames_f if s not in known_non_team and not s.startswith("_")]
print(f"Detected {len(team_sheets)} manager/team sheets")

for name in sheetnames_f:
    ws_f = wb_f[name]
    ws_d = wb_d[name] if name in wb_d.sheetnames else None

    sheet_data = {
        "state": sheet_states[name]["state"],
        "merged": merge_list(ws_f),
        "data_validations": dv_list(ws_f),
        "key_cells": {},
        "used_range": {},
    }

    # Key ranges if we know them, otherwise treat as team sheet
    ranges = dynamic_key_ranges.get(name)
    if ranges is None and name in team_sheets:
        ranges = [(1, 1, 30, 8)]  # A1:H30 for team sheets

    if ranges:
        for (r1, c1, r2, c2) in ranges:
            sheet_data["key_cells"].update(dump_ws_range(ws_f, ws_d, r1, c1, r2, c2))

    # Blind used-range dump for every sheet
    sheet_data["used_range"] = dump_used_range(ws_f, ws_d)

    extracted["sheets"][name] = sheet_data

    # Also write per-sheet JSON
    safe_name = "".join(ch if ch.isalnum() or ch in " _-" else "_" for ch in name).strip()
    with open(os.path.join(OUTPUT_DIR, SHEETS_SUBDIR, f"{safe_name}.json"), "w", encoding="utf-8") as fh:
        json.dump(sheet_data, fh, indent=2, default=str)

# =========================================================
# WRITE JSON
# =========================================================
json_path = os.path.join(OUTPUT_DIR, "extracted_data.json")
with open(json_path, "w", encoding="utf-8") as fh:
    json.dump(extracted, fh, indent=2, default=str)

# =========================================================
# WRITE HUMAN-READABLE SUMMARY
# =========================================================
summary_path = os.path.join(OUTPUT_DIR, "summary.txt")
with open(summary_path, "w", encoding="utf-8") as fh:
    def w(line=""): fh.write(line + "\n")

    w("=" * 70)
    w("FANTASY LEAGUE — EXTRACTION SUMMARY")
    w("=" * 70)
    w(f"Extracted: {datetime.now().isoformat()}")
    w(f"Workbook:  {WORKBOOK}")
    w()

    w("SHEETS (in order)")
    w("-" * 70)
    for i, n in enumerate(sheetnames_f):
        info = sheet_states[n]
        w(f"  {i:>2}. [{info['state']:<10}] {n}")
    w()

    w("NAMED RANGES")
    w("-" * 70)
    for n, d in named_ranges.items():
        w(f"  {n:<22} → {d.get('value','?')}")
    w()

    # Key sheet contents — compact
    def dump_sheet_preview(sheet_name, title, max_rows=30):
        if sheet_name not in extracted["sheets"]:
            w(f"{title}: NOT FOUND")
            w()
            return
        sd = extracted["sheets"][sheet_name]
        w(f"{title}")
        w("-" * 70)
        if not sd["key_cells"]:
            w("  (no key cells extracted)")
            w()
            return
        # Group by row for readability
        rows_seen = {}
        for ref, cell in sd["key_cells"].items():
            r = int("".join(ch for ch in ref if ch.isdigit()))
            rows_seen.setdefault(r, []).append((ref, cell))
        for r in sorted(rows_seen.keys())[:max_rows]:
            parts = []
            for ref, cell in sorted(rows_seen[r], key=lambda x: (len(x[0]), x[0])):
                v = cell.get("v")
                f = cell.get("f")
                if v is not None and f is not None:
                    parts.append(f"{ref}={v!r} ({f})")
                elif v is not None:
                    parts.append(f"{ref}={v!r}")
                elif f is not None:
                    parts.append(f"{ref}={f}")
            if parts:
                w(f"  R{r}: " + " | ".join(parts))
        w()

    dump_sheet_preview("SETTINGS",    "SETTINGS — key cells")
    dump_sheet_preview("MASTER DATA", "MASTER DATA — key cells")
    dump_sheet_preview("TEST RESULTS","TEST RESULTS — key cells")
    dump_sheet_preview("CALCULATIONS","CALCULATIONS — key cells (hidden)")
    dump_sheet_preview("RAW RESULTS", "RAW RESULTS — key cells (hidden)")
    dump_sheet_preview("POINTS HISTORY","POINTS HISTORY — key cells (hidden)")

    if overall_name:
        dump_sheet_preview(overall_name, f"{overall_name} — key cells")
    if gw_name:
        dump_sheet_preview(gw_name, f"{gw_name} — key cells")

    dump_sheet_preview("HOME", "HOME — key cells")
    dump_sheet_preview("PLAYER MARKET", "PLAYER MARKET — key cells")

    # Team sheets
    w("TEAM SHEETS")
    w("-" * 70)
    for name in team_sheets:
        sd = extracted["sheets"].get(name, {})
        picks = []
        for r in range(10, 15):
            v = sd.get("key_cells", {}).get(f"C{r}", {}).get("v")
            if v:
                picks.append(str(v))
        cap = sd.get("key_cells", {}).get("C5", {}).get("v")
        w(f"  {name:<22} captain={cap!r}  picks={picks}")
    w()

    w("NOTES")
    w("-" * 70)
    w("  - Values shown may be 'None' if Excel hadn't recalculated the file before saving.")
    w("  - Formula strings (starting with '=') appear after the value in brackets.")
    w("  - Full data: extracted_data.json")
    w("  - Per-sheet dumps: sheets/ subdirectory")
    w()

print()
print("=" * 62)
print("DONE")
print("=" * 62)
print(f"JSON:    {json_path}")
print(f"Summary: {summary_path}")
print(f"States:  {os.path.join(OUTPUT_DIR, 'sheet_states.txt')}")
print(f"Per-sheet dumps: {os.path.join(OUTPUT_DIR, SHEETS_SUBDIR)}\\")
print()
print("Next: send me summary.txt (or extracted_data.json if it's small).")