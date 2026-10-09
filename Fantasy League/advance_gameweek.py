# advance_gameweek.py  (v2 — Python-computed, cache-free)
# Archives the current GW into POINTS HISTORY + RAW RESULTS + PLAYER HISTORY,
# runs price changes from SETTINGS!C16 onwards, clears team sheets and TEST
# RESULTS, bumps CurrentGW. All scores computed in Python from source cells.
#
# Usage:
#   python advance_gameweek.py           # interactive
#   python advance_gameweek.py --yes     # no prompt

import os
import sys
import shutil
import traceback
from datetime import datetime
from openpyxl import load_workbook

# ---------- CONFIG ----------
WB_PATH = r"C:\Users\chine\OneDrive\Copies School Fantasy League for editing\11O Fantasy League.xlsx"
BACKUP_DIR = r"C:\Users\chine\OneDrive\Copies School Fantasy League for editing\backups"
LOG_PATH = r"C:\Users\chine\OneDrive\Copies School Fantasy League for editing\fantasy_patch.log"

MGR_ROW_START = 2
MGR_ROW_END = 22
GW_COL_START = 3           # C = GW1
PLAYER_SLOTS = 30
TEST_START = 6
TEST_END = 35
TEST_FIRST_COL = 3         # C
TEST_LAST_COL = 7          # G
SET_PLAYER_START = 22
SET_PLAYER_END = 51
SET_LOG_START = 55         # first player row in WEEKLY PRICE LOG
SET_LOG_COL_START = 3      # C = GW1 in the log

CONFIRM = "--yes" not in sys.argv

# ---------- LOGGING ----------
def log(msg):
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line)
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        pass

def backup(path):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(os.path.basename(path))
    dest = os.path.join(BACKUP_DIR, f"{name}_pre_advance_{stamp}{ext}")
    shutil.copy2(path, dest)
    log(f"Backup: {dest}")

def col_letter(n):
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s

# ---------- MAIN ----------
def main():
    log("=" * 60)
    log("ADVANCE GAMEWEEK — START")

    if not os.path.exists(WB_PATH):
        log(f"ERROR: {WB_PATH} not found"); sys.exit(1)

    log(f"Loading {WB_PATH}")
    wb = load_workbook(WB_PATH, data_only=False)

    settings = wb["SETTINGS"]
    calc = wb["CALCULATIONS"]
    ph = wb["POINTS HISTORY"]
    raw = wb["RAW RESULTS"]
    phist = wb["PLAYER HISTORY"]

    # --- Read config ---
    current_gw = wb.defined_names["CurrentGW"].attr_text
    # attr_text like SETTINGS!$C$87
    ref = current_gw.replace("$", "").split("!")
    cur_sheet, cur_cell = ref[0].strip("'"), ref[1]
    current_gw = int(settings[cur_cell].value)

    season_len = int(wb.defined_names["SeasonLength"].attr_text.replace("$","").split("!")[1].replace("C","")) # rough
    season_len = int(settings.cell(int(wb.defined_names["SeasonLength"].attr_text.replace("$","").split("!")[1][1:]), 3).value)

    log(f"CurrentGW = {current_gw}, SeasonLength = {season_len}")
    if current_gw > season_len:
        log("Season already complete.")
        sys.exit(0)
    if CONFIRM:
        ans = input(f"Advance from GW{current_gw} to GW{current_gw+1}? [y/N] ").strip().lower()
        if ans not in ("y", "yes"):
            log("Aborted."); sys.exit(0)

    backup(WB_PATH)

    # --- Read rules ---
    base_score = settings["C5"].value
    step_div   = settings["C6"].value
    score_min  = settings["C7"].value
    score_max  = settings["C8"].value
    max_delta  = settings["C9"].value
    tier_low   = settings["C10"].value
    tier_mid   = settings["C11"].value
    tier_high  = settings["C12"].value
    price_step = settings["C13"].value
    min_price  = settings["C14"].value
    max_price  = settings["C15"].value
    price_start_gw = int(settings["C16"].value)
    tests_per_gw = int(settings["C17"].value)
    captain_mult = settings["C18"].value

    # --- Read TEST RESULTS raw scores ---
    tr = wb["TEST RESULTS"]
    player_raw = {}   # name -> avg of first N test slots (None if empty)
    for r in range(TEST_START, TEST_END + 1):
        nm = tr.cell(r, 2).value
        if not nm:
            continue
        vals = []
        for c in range(TEST_FIRST_COL, TEST_FIRST_COL + tests_per_gw):
            v = tr.cell(r, c).value
            if isinstance(v, (int, float)):
                vals.append(v)
        player_raw[nm] = (sum(vals) / len(vals)) if vals else None

    # --- Compute per-player fantasy points ---
    scored = {nm: v for nm, v in player_raw.items() if v is not None}
    if not scored:
        log("ERROR: no scores entered in TEST RESULTS."); sys.exit(1)
    class_avg = sum(scored.values()) / len(scored)
    hi = max(scored.values()); lo = min(scored.values())
    step = max((hi - lo) / step_div, 0.1)

    player_points = {}
    for nm, raw_score in player_raw.items():
        if raw_score is None:
            player_points[nm] = 0
            continue
        pts = base_score + int((raw_score - class_avg) // step)
        pts = max(score_min, min(score_max, pts))
        player_points[nm] = pts

    # --- Compute per-manager GW scores ---
    managers = []
    for r in range(MGR_ROW_START, MGR_ROW_END + 1):
        managers.append(calc.cell(r, 11).value)   # K = manager name

    gw_scores = {}
    for i, m in enumerate(managers):
        r = MGR_ROW_START + i
        picks = [calc.cell(r, c).value for c in range(12, 17)]  # L..P
        cap = calc.cell(r, 17).value  # Q
        status = calc.cell(r, 21).value  # U
        if status != "VALID TEAM":
            gw_scores[m] = 0
            continue
        total = 0
        for p in picks:
            total += player_points.get(p, 0)
        if cap and cap in player_points:
            total += player_points[cap] * (captain_mult - 1)
        gw_scores[m] = total

    log(f"Computed GW scores for {len(gw_scores)} managers.")

    # --- Write RAW RESULTS + POINTS HISTORY ---
    col = GW_COL_START + (current_gw - 1)
    log(f"Writing GW{current_gw} into column {col_letter(col)} of RAW + POINTS HISTORY")
    for i, m in enumerate(managers):
        r = MGR_ROW_START + i
        raw.cell(r, col).value = gw_scores[m]
        ph.cell(r, col).value  = gw_scores[m]

    # --- Write PLAYER HISTORY raw scores ---
    log(f"Writing GW{current_gw} player raw scores into PLAYER HISTORY")
    for i in range(PLAYER_SLOTS):
        r = 2 + i
        pname = phist.cell(r, 2).value
        if not pname:
            continue
        score = player_raw.get(pname)
        phist.cell(r, col).value = score

    # --- Price changes from price_start_gw onwards ---
    if current_gw >= price_start_gw:
        log(f"Running price changes (GW{current_gw} >= start GW{price_start_gw})")
        run_price_changes(wb, phist, settings, current_gw)
    else:
        log(f"Prices not active until GW{price_start_gw} — skipping.")

    # --- Clear team sheets + TEST RESULTS ---
    log("Clearing team sheets and TEST RESULTS...")
    for m in managers:
        ws = wb[m]
        ws["C5"].value = None
        for r in range(10, 15):
            ws.cell(r, 3).value = None
    for r in range(TEST_START, TEST_END + 1):
        for c in range(TEST_FIRST_COL, TEST_LAST_COL + 1):
            tr.cell(r, c).value = None
    log("  done")

    # --- Bump CurrentGW ---
    # Find "Current GW" label row in SETTINGS
    cgw_row = None
    for r in range(80, 100):
        if settings.cell(r, 2).value == "Current GW":
            cgw_row = r; break
    if cgw_row is None:
        log("ERROR: could not find 'Current GW' label in SETTINGS"); sys.exit(1)
    settings.cell(cgw_row, 3).value = current_gw + 1
    log(f"CurrentGW bumped: {current_gw} -> {current_gw+1}")

    # --- Save ---
    wb.save(WB_PATH)
    log(f"Saved: {WB_PATH}")
    log(f"ADVANCE COMPLETE — now at GW{current_gw+1}")
    log("=" * 60)

# ---------- PRICE ENGINE ----------
def run_price_changes(wb, phist, settings, current_gw):
    """
    For each player, compute:
      - 3-week rolling avg of raw scores (columns C..V of PLAYER HISTORY, last 3 weeks)
      - class 3-week avg
      - gap = player_avg - class_avg
      - delta ladder based on gap / 10 (1 step = 10 pp), capped at ±0.5
      - tier multiplier by CURRENT price
      - write delta into SETTINGS WEEKLY PRICE LOG
      - update PLAYER HISTORY audit columns W/X/Y
    """
    max_delta  = settings["C9"].value
    tier_low   = settings["C10"].value
    tier_mid   = settings["C11"].value
    tier_high  = settings["C12"].value
    price_step = settings["C13"].value
    min_price  = settings["C14"].value
    max_price  = settings["C15"].value

    # Determine the window: current_gw-2 .. current_gw  (3 weeks inclusive)
    first_week = max(1, current_gw - 2)
    week_cols = [GW_COL_START + w - 1 for w in range(first_week, current_gw + 1)]

    # Gather each player's 3-week average
    player_avgs = {}
    for i in range(PLAYER_SLOTS):
        r = 2 + i
        pname = phist.cell(r, 2).value
        if not pname:
            continue
        scores = [phist.cell(r, c).value for c in week_cols]
        scores = [s for s in scores if isinstance(s, (int, float))]
        if scores:
            player_avgs[pname] = sum(scores) / len(scores)
        else:
            player_avgs[pname] = None

    valid = [v for v in player_avgs.values() if v is not None]
    class_avg_3 = sum(valid) / len(valid) if valid else 0.0

    # Apply deltas
    for i in range(PLAYER_SLOTS):
        r = 2 + i
        pname = phist.cell(r, 2).value
        if not pname:
            continue
        p_avg = player_avgs.get(pname)
        # Write audit columns W/X/Y
        phist.cell(r, 23).value = round(p_avg, 2) if p_avg is not None else None
        phist.cell(r, 24).value = round(class_avg_3, 2)
        gap = (p_avg - class_avg_3) if p_avg is not None else None
        phist.cell(r, 25).value = round(gap, 2) if gap is not None else None

        if gap is None:
            continue
        # Delta ladder: 1 step = 10 pp
        steps = gap / 10.0
        if steps >= 5:      delta = 0.5
        elif steps >= 4:    delta = 0.4
        elif steps >= 3:    delta = 0.3
        elif steps >= 2:    delta = 0.2
        elif steps >= 1:    delta = 0.1
        elif steps > -1:    delta = 0.0
        elif steps > -2:    delta = -0.1
        elif steps > -3:    delta = -0.2
        elif steps > -4:    delta = -0.3
        elif steps > -5:    delta = -0.4
        else:               delta = -0.5

        # Cap
        delta = max(-max_delta, min(max_delta, delta))

        # Tier multiplier based on current price
        cur_price = settings.cell(SET_PLAYER_START + i, 6).value  # F = Final
        if cur_price is None:
            continue
        if cur_price < 9.0:
            mult = tier_low
        elif cur_price < 11.0:
            mult = tier_mid
        else:
            mult = tier_high
        delta *= mult

        # Round to price_step (0.1)
        delta = round(delta / price_step) * price_step

        # Write to WEEKLY PRICE LOG
        log_row = SET_LOG_START + i
        log_col = SET_LOG_COL_START + (current_gw - 1)
        settings.cell(log_row, log_col).value = delta

    log(f"  price changes applied for GW{current_gw} (class avg {class_avg_3:.1f})")

# ---------- RUN ----------
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        log("FATAL ERROR:")
        log(traceback.format_exc())
        sys.exit(1)