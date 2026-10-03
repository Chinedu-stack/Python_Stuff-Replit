# =========================================================
# advance_gameweek.py — Advance one gameweek
# Reads GW from named range CurrentGW, season length from
# SeasonLength, captain mult from SETTINGS!C18.
# Clears team sheets + TEST RESULTS inputs.
# Rewires Overall Leaderboard to use CALCULATIONS!W.
# Handles price changes (start week from SETTINGS!C16).
# =========================================================
import os
import sys
import glob
import shutil
import logging
from datetime import datetime
from contextlib import contextmanager

import openpyxl
from openpyxl.utils import get_column_letter, coordinate_to_tuple

# =========================================================
# CONFIG
# =========================================================
FILE_PATH  = r"C:\Users\chine\OneDrive\Copies School Fantasy League for editing\11O Fantasy League.xlsx"
BACKUP_DIR = r"C:\Users\chine\OneDrive\Copies School Fantasy League for editing"
PASSWORD   = "Legendx24j@"
BACKUPS_TO_KEEP = 20
LOG_PATH   = os.path.join(BACKUP_DIR, "fantasy_patch.log")

AUTO_CONFIRM = "--yes" in sys.argv or "-y" in sys.argv

# Sheet names (exact, including the leading space in Overall)
TR_SHEET   = "TEST RESULTS"
RR_SHEET   = "RAW RESULTS"
MD_SHEET   = "MASTER DATA"
PH_SHEET   = "POINTS HISTORY"
CALC_SHEET = "CALCULATIONS"
OVR_SHEET  = " Overall Leaderboard"   # NOTE: leading space
SET_SHEET  = "SETTINGS"

# TEST RESULTS layout
TR_NAME_C     = 2     # B
TR_SCORE_C    = 8     # H
TR_FIRST      = 6
TR_INPUT_COLS = range(3, 8)   # C..G (5 test-input columns)

# RAW RESULTS layout
RR_NAME_C = 2         # B
RR_FIRST  = 2

# POINTS HISTORY layout
PH_NAME_C = 2         # B
PH_FIRST  = 2

# MASTER DATA layout
MD_NAME_C = 2         # B
MD_FIRST  = 2

# CALCULATIONS layout
CALC_MGR_C = 11       # K  (manager names)
CALC_GW_C  = 20       # T  (GW score)
CALC_OVR_C = 23       # W  (overall total)
CALC_FIRST = 2

# Team sheet layout
TEAM_CAPTAIN   = "C5"
TEAM_PICK_ROWS = [10, 11, 12, 13, 14]
TEAM_PICK_C    = 3    # C

# =========================================================
# LOGGING
# =========================================================
logging.basicConfig(
    filename=LOG_PATH, level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("advance")
_console = logging.StreamHandler(sys.stdout)
_console.setFormatter(logging.Formatter("%(message)s"))
log.addHandler(_console)

# =========================================================
# HELPERS
# =========================================================
def last_row(ws, col, start=1):
    r = start
    while ws.cell(r, col).value not in (None, ""):
        r += 1
    return r - 1

@contextmanager
def unprotected(ws, password=PASSWORD):
    was = ws.protection.sheet
    if was:
        ws.protection.sheet = False
    try:
        yield ws
    finally:
        if was:
            ws.protection.sheet = True
            ws.protection.password = password

def make_backup():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(BACKUP_DIR, f"11O Fantasy League_backup_{ts}.xlsx")
    shutil.copy2(FILE_PATH, path)
    return path

def prune_backups(keep=BACKUPS_TO_KEEP):
    files = sorted(glob.glob(os.path.join(BACKUP_DIR, "*_backup_*.xlsx")),
                   key=os.path.getmtime, reverse=True)
    for f in files[keep:]:
        try: os.remove(f)
        except OSError: pass

def named_cell(wb, name):
    if name not in wb.defined_names:
        return None
    ref = wb.defined_names[name].attr_text
    if "!" not in ref:
        return None
    sheet, cell = ref.split("!", 1)
    sheet = sheet.strip("'")
    cell = cell.replace("$", "")
    r, c = coordinate_to_tuple(cell)
    return sheet, r, c

def read_named(wb, name, default=None):
    info = named_cell(wb, name)
    if not info:
        return default
    sheet, r, c = info
    if sheet not in wb.sheetnames:
        return default
    v = wb[sheet].cell(r, c).value
    return v if v not in (None, "") else default

def write_named(wb, name, value):
    info = named_cell(wb, name)
    if not info:
        raise RuntimeError(f"Named range {name} not found")
    sheet, r, c = info
    ws = wb[sheet]
    with unprotected(ws):
        ws.cell(r, c, value)

def get_delta(gap):
    if gap >= 10:  return 0.5
    if gap >= 7:   return 0.4
    if gap >= 4:   return 0.3
    if gap >= 1:   return 0.2
    if gap > 0:    return 0.1
    if gap == 0:   return 0.0
    if gap > -1:   return -0.1
    if gap > -4:   return -0.2
    if gap > -7:   return -0.3
    if gap > -10:  return -0.4
    return -0.5

# =========================================================
# MAIN
# =========================================================
def main():
    log.info("=" * 62)
    log.info("ADVANCE GAMEWEEK")
    log.info("=" * 62)

    if not os.path.exists(FILE_PATH):
        raise FileNotFoundError(FILE_PATH)

    # Load twice: data_only for computed values, editable for writing
    wb_v = openpyxl.load_workbook(FILE_PATH, data_only=True)
    wb   = openpyxl.load_workbook(FILE_PATH)

    s = wb[SET_SHEET]
    current_gw   = int(read_named(wb_v, "CurrentGW", 1) or 1)
    total_weeks  = int(read_named(wb_v, "SeasonLength", 20) or 20)
    captain_mult = int(s["C18"].value or 2)

    log.info("Current GW: %d / %d   Captain ×%d",
             current_gw, total_weeks, captain_mult)

    if current_gw >= total_weeks:
        log.error("Already at final week. Nothing to advance.")
        return

    # --- Read scores from TEST RESULTS ---
    tr_v = wb_v[TR_SHEET]
    tr_last = last_row(tr_v, TR_NAME_C, start=TR_FIRST)
    if tr_last < TR_FIRST:
        log.error("No students in TEST RESULTS.")
        return

    scores = {}
    for r in range(TR_FIRST, tr_last + 1):
        n = tr_v.cell(r, TR_NAME_C).value
        if not n:
            continue
        v = tr_v.cell(r, TR_SCORE_C).value
        scores[str(n).strip()] = v

    filled = sum(1 for v in scores.values() if v not in (None, ""))
    log.info("Scores: %d filled / %d students", filled, len(scores))

    if filled == 0:
        log.error("No scores entered in TEST RESULTS!H. Aborting.")
        log.error("(If you did enter them, open the file in Excel, save,")
        log.error(" close, then re-run so formula caches are up to date.)")
        return

    # --- Read manager GW scores from CALCULATIONS!T ---
    calc_v = wb_v[CALC_SHEET]
    calc_mgr_last = last_row(calc_v, CALC_MGR_C, start=CALC_FIRST)
    if calc_mgr_last < CALC_FIRST:
        log.error("No managers found in CALCULATIONS!K.")
        return

    manager_gw = {}
    for r in range(CALC_FIRST, calc_mgr_last + 1):
        n = calc_v.cell(r, CALC_MGR_C).value
        if not n:
            continue
        raw = calc_v.cell(r, CALC_GW_C).value
        try:
            val = int(round(float(raw)))
        except (TypeError, ValueError):
            val = 0
        manager_gw[str(n).strip()] = val

    log.info("Manager GW scores: %d managers", len(manager_gw))

    # --- Confirm ---
    next_gw = current_gw + 1
    if not AUTO_CONFIRM:
        print()
        print(f"Advance from Week {current_gw} to Week {next_gw}?")
        resp = input("Type Y to continue: ").strip().upper()
        if resp != "Y":
            print("Cancelled.")
            return
        print()

    # --- Backup + rollback guard ---
    backup = make_backup()
    log.info("[OK] Backup: %s", os.path.basename(backup))

    try:
        _do_advance(wb, current_gw, next_gw, total_weeks,
                    scores, manager_gw)

        try:
            wb.save(FILE_PATH)
        except PermissionError:
            log.error("Could not save — is the workbook open in Excel?")
            raise

        log.info("[OK] Saved: %s", FILE_PATH)
        prune_backups()
        log.info("=" * 62)
        log.info("DONE. Now on GW%d.", next_gw)

    except Exception:
        log.exception("Advance failed — restoring backup")
        try:
            shutil.copy2(backup, FILE_PATH)
            log.info("[OK] Rolled back from backup")
        except Exception:
            log.exception("Rollback ALSO failed — manual recovery required")
        raise


# =========================================================
# THE ADVANCE
# =========================================================
def _do_advance(wb, current_gw, next_gw, total_weeks, scores, manager_gw):
    s    = wb[SET_SHEET]
    tr   = wb[TR_SHEET]
    rr   = wb[RR_SHEET]
    ph   = wb[PH_SHEET]

    gw_col = 2 + current_gw   # column index: GW1 = C (3), GW2 = D (4), ...

    # ---- 1. Archive scores into RAW RESULTS ----
    with unprotected(rr):
        rr_last = last_row(rr, RR_NAME_C, start=RR_FIRST)
        if rr_last < RR_FIRST:
            raise RuntimeError("RAW RESULTS has no rows")

        already = any(
            rr.cell(r, gw_col).value not in (None, "")
            for r in range(RR_FIRST, rr_last + 1)
        )
        if already:
            log.warning("GW%d already has data in RAW RESULTS.", current_gw)
            if AUTO_CONFIRM:
                log.info("--yes flag: overwriting.")
            else:
                resp = input("Overwrite? [Y/N]: ").strip().upper()
                if resp != "Y":
                    raise RuntimeError("Cancelled by user")

        archived = 0
        for r in range(RR_FIRST, rr_last + 1):
            n = rr.cell(r, RR_NAME_C).value
            if not n:
                continue
            v = scores.get(str(n).strip())
            rr.cell(r, gw_col, v)
            if v not in (None, ""):
                archived += 1
    log.info("[OK] Archived %d scores into RAW RESULTS GW%d",
             archived, current_gw)

    # ---- 2. Write manager totals to POINTS HISTORY ----
    with unprotected(ph):
        ph_last = last_row(ph, PH_NAME_C, start=PH_FIRST)
        if ph_last < PH_FIRST:
            raise RuntimeError("POINTS HISTORY has no managers")

        ph_rows = {}
        for r in range(PH_FIRST, ph_last + 1):
            n = ph.cell(r, PH_NAME_C).value
            if n:
                ph_rows[str(n).strip()] = r

        written = 0
        for name, pts in manager_gw.items():
            if name not in ph_rows:
                log.warning("Manager %s not in POINTS HISTORY, skipping", name)
                continue
            ph.cell(ph_rows[name], gw_col, pts)
            written += 1
    log.info("[OK] POINTS HISTORY GW%d written (%d managers)",
             current_gw, written)

    # ---- 3. Rewire Overall Leaderboard to use CALCULATIONS!W ----
    _rewire_overall(wb)

    # ---- 4. Price changes (if eligible) ----
    start_week = int(s["C16"].value or 3)
    if current_gw >= start_week:
        _do_prices(wb, current_gw, total_weeks)
    else:
        log.info("Price changes skipped (start week = %d)", start_week)

    # ---- 5. Clear team sheets ----
    _clear_team_sheets(wb)

    # ---- 6. Clear TEST RESULTS inputs (C..G) ----
    with unprotected(tr):
        tr_last = last_row(tr, TR_NAME_C, start=TR_FIRST)
        for r in range(TR_FIRST, tr_last + 1):
            if not tr.cell(r, TR_NAME_C).value:
                continue
            for c in TR_INPUT_COLS:
                tr.cell(r, c, None)
    log.info("[OK] TEST RESULTS inputs cleared")

    # ---- 7. Bump CurrentGW ----
    write_named(wb, "CurrentGW", next_gw)
    log.info("[OK] GW advanced: %d → %d", current_gw, next_gw)


# =========================================================
# OVERALL LEADERBOARD — rewire to use CALCULATIONS!W
# =========================================================
def _rewire_overall(wb):
    if OVR_SHEET not in wb.sheetnames:
        log.warning("Overall Leaderboard '%s' not found.", OVR_SHEET)
        return
    ovr = wb[OVR_SHEET]
    calc = wb[CALC_SHEET]

    n = last_row(calc, CALC_MGR_C, start=CALC_FIRST) - CALC_FIRST + 1
    if n <= 0:
        log.warning("No managers in CALCULATIONS!K.")
        return

    first, last = CALC_FIRST, CALC_FIRST + n - 1
    top = 5 + n

    with unprotected(ovr):
        ovr["B3"] = (
            f'=IF(MAX($D$6:$D${top})=0,"🏆  OVERALL LEADER:  No results yet",'
            f'"🏆  OVERALL LEADER:  "&INDEX($C$6:$C${top},'
            f'MATCH(MAX($D$6:$D${top}),$D$6:$D${top},0))&"  —  "&MAX($D$6:$D${top})&" pts")'
        )
        for i in range(n):
            r = 6 + i
            ovr.cell(r, 3,
                f'=IFERROR(INDEX(CALCULATIONS!$K${first}:$K${last},'
                f'MATCH(LARGE(CALCULATIONS!$W${first}:$W${last},ROW()-5),'
                f'CALCULATIONS!$W${first}:$W${last},0)),"")')
            ovr.cell(r, 4,
                f"=ROUND(LARGE(CALCULATIONS!$W${first}:$W${last},ROW()-5),0)")
    log.info("[OK] Overall Leaderboard rewired to use CALCULATIONS!W")


# =========================================================
# PRICE CHANGES
# =========================================================
def _do_prices(wb, current_gw, total_weeks):
    s = wb[SET_SHEET]

    max_change = float(s["C9"].value  or 0.5)
    mult_low   = float(s["C10"].value or 1.0)
    mult_mid   = float(s["C11"].value or 0.75)
    mult_high  = float(s["C12"].value or 0.5)
    min_price  = float(s["C14"].value or 7.0)
    max_price  = float(s["C15"].value or 13.0)

    # Locate sections (PLAYER PRICES header and WEEKLY PRICE LOG header)
    pp_hdr = pl_hdr = None
    for r in range(1, 300):
        v = s.cell(r, 2).value
        if v == "PLAYER PRICES":
            pp_hdr = r
        if isinstance(v, str) and v.startswith("WEEKLY PRICE LOG"):
            pl_hdr = r

    if not pp_hdr or not pl_hdr:
        log.warning("Could not find PLAYER PRICES or WEEKLY PRICE LOG. Skipping prices.")
        return

    pp_first = pp_hdr + 2   # data row after column headers
    pl_first = pl_hdr + 2

    # Build player list (name, price_row, log_row)
    players = []
    for i, r in enumerate(range(pp_first, pp_first + 200)):
        n = s.cell(r, 2).value
        if n is None:
            break
        players.append((str(n).strip(), r, pl_first + i))

    log.info("  Found %d players in price table", len(players))

    # --- Read all raw scores up to this GW ---
    rr = wb[RR_SHEET]
    rr_last = last_row(rr, RR_NAME_C, start=RR_FIRST)
    raw_data = {}
    for r in range(RR_FIRST, rr_last + 1):
        n = rr.cell(r, RR_NAME_C).value
        if not n:
            continue
        n = str(n).strip()
        raw_data[n] = {w: rr.cell(r, 2 + w).value
                       for w in range(1, current_gw + 1)}

    # --- Current prices (base + cumulative or override) ---
    current_prices = {}
    for name, prow, lrow in players:
        base     = s.cell(prow, 3).value or 0
        override = s.cell(prow, 5).value
        cum = 0.0
        for w in range(1, current_gw + 1):
            v = s.cell(lrow, 2 + w).value
            if isinstance(v, (int, float)):
                cum += v
        if override not in (None, ""):
            price = float(override)
        else:
            price = max(min_price, min(max_price, base + cum))
        current_prices[name] = price

    # --- 3-week rolling window ---
    weeks = [w for w in range(current_gw - 2, current_gw + 1) if w >= 1]

    class_vals = []
    for w in weeks:
        for name in raw_data:
            v = raw_data[name].get(w)
            if v not in (None, ""):
                class_vals.append(v)
    class_avg_3w = sum(class_vals) / len(class_vals) if class_vals else 0
    log.info("  Class 3-week avg: %.2f", class_avg_3w)

    # --- Compute deltas ---
    deltas = {}
    for name, prow, lrow in players:
        vals = [raw_data.get(name, {}).get(w) for w in weeks]
        vals = [v for v in vals if v not in (None, "")]
        if not vals:
            deltas[name] = 0.0
            continue
        gap = (sum(vals) / len(vals)) - class_avg_3w
        raw_d = get_delta(gap)
        price = current_prices.get(name, 10.0)
        if price < 9.0:
            mult = mult_low
        elif price < 11.0:
            mult = mult_mid
        else:
            mult = mult_high
        adj = raw_d * mult
        adj = max(-max_change, min(max_change, adj))
        deltas[name] = round(adj * 10) / 10

    # --- Write deltas into WEEKLY PRICE LOG column for this GW ---
    gw_col = 2 + current_gw
    for name, prow, lrow in players:
        c = s.cell(lrow, gw_col)
        c.value = deltas[name]
        c.number_format = '+£0.0"m";-£0.0"m";—'

    # --- Rewrite cumulative formula column D (points to correct log row) ---
    last_letter = get_column_letter(2 + total_weeks)
    for name, prow, lrow in players:
        s.cell(prow, 4, f"=SUM(C{lrow}:{last_letter}{lrow})")

    movers = sorted(deltas.items(), key=lambda x: -abs(x[1]))[:5]
    log.info("[OK] Price deltas written for GW%d", current_gw)
    for name, d in movers:
        log.info("    %s: %+0.1f", name, d)


# =========================================================
# CLEAR TEAM SHEETS (picks + captain)
# =========================================================
def _clear_team_sheets(wb):
    md = wb[MD_SHEET]
    md_last = last_row(md, MD_NAME_C, start=MD_FIRST)

    cleared = 0
    for r in range(MD_FIRST, md_last + 1):
        n = md.cell(r, MD_NAME_C).value
        if not n:
            continue
        name = str(n).strip()
        if name not in wb.sheetnames:
            log.warning("No sheet for manager %s — skipping.", name)
            continue
        ws = wb[name]
        with unprotected(ws):
            ws[TEAM_CAPTAIN] = None
            for row in TEAM_PICK_ROWS:
                ws.cell(row, TEAM_PICK_C, None)
        cleared += 1
    log.info("[OK] Cleared picks+captain on %d team sheets", cleared)


if __name__ == "__main__":
    main()