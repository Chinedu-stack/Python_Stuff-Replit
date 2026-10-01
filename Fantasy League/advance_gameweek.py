import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment, Protection
import shutil
import os
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================
FILE_PATH = r"C:\Users\chine\OneDrive\Python Stuff\Fantasy League\Year_11_Fantasy_League_v2.xlsx"
BACKUP_DIR = r"C:\Users\chine\OneDrive\Python Stuff\Fantasy League"
TOTAL_WEEKS = 20

# =========================================================
# HELPERS
# =========================================================
def get_delta(gap):
    if gap >= 10: return 0.5
    if gap >= 7: return 0.4
    if gap >= 4: return 0.3
    if gap >= 1: return 0.2
    if gap > 0: return 0.1
    if gap == 0: return 0.0
    if gap > -1: return -0.1
    if gap > -4: return -0.2
    if gap > -7: return -0.3
    if gap > -10: return -0.4
    return -0.5

def get_multiplier(price):
    if price < 9.0: return 1.0
    if price < 11.0: return 0.75
    return 0.5

def round_tenth(x):
    return round(x * 10) / 10

# =========================================================
# MAIN
# =========================================================
def main():
    print("=" * 62)
    print("ADVANCE GAMEWEEK")
    print("=" * 62)
    print()

    # ----- Load -----
    print(f"Opening: {FILE_PATH}")
    wb = openpyxl.load_workbook(FILE_PATH)

    # ----- Read current gameweek -----
    home = wb["HOME"]
    current_gw = home["C7"].value
    try:
        current_gw = int(current_gw)
    except (TypeError, ValueError):
        print(f"ERROR: HOME!C7 is not a number (got: {current_gw})")
        return
    print(f"Current gameweek: {current_gw}")

    # ----- Read TEST RESULTS -----
    results = wb["TEST RESULTS"]
    scores = {}
    for r in range(5, 30):
        name = results.cell(r, 2).value
        score = results.cell(r, 3).value
        if name:
            scores[name.strip()] = score

    filled = sum(1 for s in scores.values() if s is not None and s != "")
    print(f"Scores to archive: {filled} of {len(scores)}")

    # ----- Price change eligibility -----
    do_prices = current_gw >= 3
    if do_prices:
        print(f"Price changes: YES (Week {current_gw} → first eligible week)")
    else:
        print(f"Price changes: NO (settling in until Week 3)")

    # ----- Confirm -----
    next_gw = current_gw + 1
    print()
    print(f"Advance from Week {current_gw} to Week {next_gw}?")
    resp = input("Type Y to continue, anything else to cancel: ").strip().upper()
    if resp != "Y":
        print("Cancelled.")
        return
    print()

    # ----- Backup -----
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"Year_11_Fantasy_League_v2_backup_{timestamp}.xlsx"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    shutil.copy2(FILE_PATH, backup_path)
    print(f"[OK] Backup saved: {backup_name}")

    # ----- Archive into RAW RESULTS -----
    raw = wb["RAW RESULTS"]
    gw_col = 2 + current_gw  # col C=3 is GW1

    # double-run check
    already = False
    for r in range(2, 100):
        if raw.cell(r, 2).value is None:
            break
        v = raw.cell(r, gw_col).value
        if v not in (None, ""):
            already = True
            break

    if already:
        print(f"WARNING: Week {current_gw} already has data in RAW RESULTS.")
        resp = input("Overwrite anyway? [Y/N]: ").strip().upper()
        if resp != "Y":
            print("Cancelled.")
            return

    archived = 0
    for r in range(2, 100):
        name = raw.cell(r, 2).value
        if not name:
            break
        name = name.strip()
        score = scores.get(name, None)
        raw.cell(r, gw_col, score)
        if score is not None and score != "":
            archived += 1
    print(f"[OK] Archived {archived} scores into GW{current_gw}")

    # ----- Read RAW data for the last 3 weeks (for prices) -----
    raw_data = {}
    for r in range(2, 100):
        name = raw.cell(r, 2).value
        if not name:
            break
        name = name.strip()
        raw_data[name] = {}
        for w in range(1, current_gw + 1):
            raw_data[name][w] = raw.cell(r, 2 + w).value

    # =====================================================
    # COMPUTE GW POINTS per manager
    # =====================================================
    # Get this week's scores only
    week_scores = {}
    for name, wdict in raw_data.items():
        week_scores[name] = wdict.get(current_gw)

    valid = [s for s in week_scores.values() if s is not None and s != ""]
    if valid:
        class_avg = sum(valid) / len(valid)
        class_range = max(valid) - min(valid)
        step = max(class_range / 10, 0.1)
    else:
        class_avg = 0
        step = 1.0

    player_pts = {}
    for name, sc in week_scores.items():
        if sc is None or sc == "":
            player_pts[name] = 0
            continue
        raw_pts = 5 + int((sc - class_avg) / step)  # int() = ROUNDDOWN toward zero
        player_pts[name] = max(0, min(10, raw_pts))

    # Get manager picks from MASTER DATA
    md = wb["MASTER DATA"]
    manager_gw = {}
    manager_picks = {}
    for r in range(2, 100):
        name = md.cell(r, 2).value
        if not name:
            break
        name = name.strip()
        picks = [md.cell(r, c).value for c in range(3, 8)]  # C-G = P1-P5
        cap = md.cell(r, 8).value  # H = captain
        manager_picks[name] = (picks, cap)

        total = 0
        for p in picks:
            if p:
                total += player_pts.get(p.strip() if isinstance(p, str) else p, 0)
        if cap:
            cap = cap.strip() if isinstance(cap, str) else cap
            total += player_pts.get(cap, 0)  # captain bonus (2x → +1x extra)
        manager_gw[name] = total

    # =====================================================
    # Write to POINTS HISTORY (create if missing)
    # =====================================================
    if "POINTS HISTORY" not in wb.sheetnames:
        ph = wb.create_sheet("POINTS HISTORY")
        ph.sheet_state = "hidden"
        ph.cell(1, 2, "Manager")
        for w in range(1, TOTAL_WEEKS + 1):
            ph.cell(1, 2 + w, f"GW{w}")
        for i, name in enumerate(manager_gw.keys()):
            ph.cell(2 + i, 2, name)
        # Format
        thin = Side(style="thin", color="E5E7EB")
        for c in range(2, 3 + TOTAL_WEEKS):
            cell = ph.cell(1, c)
            cell.font = Font(bold=True, color="FFFFFF", size=12)
            cell.fill = PatternFill("solid", fgColor="0B1F3A")
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = Border(bottom=Side(style="medium", color="1565C0"))
        ph.row_dimensions[1].height = 32
    else:
        ph = wb["POINTS HISTORY"]

    # Write this week's GW points
    ph_col = 2 + current_gw
    for i, name in enumerate(manager_gw.keys()):
        r = 2 + i
        ph.cell(r, ph_col, manager_gw[name])
    print(f"[OK] GW points written to POINTS HISTORY GW{current_gw}")

    # =====================================================
    # Update CALCULATIONS W (Overall) and X (tiebreak)
    # =====================================================
    calc = wb["CALCULATIONS"]
    calc.cell(1, 23, "Overall")  # W1
    calc.cell(1, 24, "OverallTB")  # X1
    for r in range(2, 2 + len(manager_gw)):
        name = calc.cell(r, 11).value  # K column = Manager
        # W = sum of this manager's row in POINTS HISTORY
        calc.cell(r, 23, f"=SUM('POINTS HISTORY'!C{r}:{chr(ord('C')+TOTAL_WEEKS-1)}{r})")
        # X = W + tiebreak
        calc.cell(r, 24, f"=W{r}+ROW()/10000")
    print(f"[OK] CALCULATIONS W/X columns updated")

    # =====================================================
    # Rewrite OVERALL Leaderboard formulas to use X
    # =====================================================
    overall = wb["2. Overall Leaderboard"]
    overall["B3"] = ('=IF(MAX($D$6:$D$26)=0,"No results yet","OVERALL LEADER: "'
                     '&INDEX($C$6:$C$26,MATCH(MAX($D$6:$D$26),$D$6:$D$26,0))'
                     '&" — "&MAX($D$6:$D$26)&" pts")')
    for i in range(21):
        r = 6 + i
        overall.cell(r, 2, f"=SUMPRODUCT((D$6:D$26>D{r})/COUNTIF(D$6:D$26,D$6:D$26))+1")
        overall.cell(r, 3, f'=IFERROR(INDEX(CALCULATIONS!$K$2:$K$22,'
                           f'MATCH(LARGE(CALCULATIONS!$X$2:$X$22,ROW()-5),'
                           f'CALCULATIONS!$X$2:$X$22,0)),"")')
        overall.cell(r, 4, f"=ROUND(LARGE(CALCULATIONS!$X$2:$X$22,ROW()-5),0)")
    print(f"[OK] Overall Leaderboard rewired to use X (overall points)")

    # =====================================================
    # Price changes (only GW3+)
    # =====================================================
    if do_prices:
        settings = wb["SETTINGS"]

        # Locate sections in SETTINGS
        pp_header_row = None
        pl_header_row = None
        for r in range(1, 200):
            v = settings.cell(r, 2).value
            if v == "PLAYER PRICES":
                pp_header_row = r + 1
            if v and isinstance(v, str) and v.startswith("WEEKLY PRICE LOG"):
                pl_header_row = r + 1

        if not pp_header_row or not pl_header_row:
            print("ERROR: Could not find SETTINGS sections. Skipping prices.")
        else:
            pp_data_start = pp_header_row + 1
            pl_data_start = pl_header_row + 1

            # Gather player names
            player_list = []
            for r in range(pp_data_start, pp_data_start + 100):
                n = settings.cell(r, 2).value
                if n is None:
                    break
                player_list.append((r, n.strip()))

            # Compute current prices
            current_prices = {}
            for i, (pp_row, name) in enumerate(player_list):
                base = settings.cell(pp_row, 3).value or 0
                override = settings.cell(pp_row, 5).value
                log_row = pl_data_start + i
                cum = 0.0
                for w in range(1, current_gw + 1):
                    v = settings.cell(log_row, 2 + w).value
                    if isinstance(v, (int, float)):
                        cum += v
                if override not in (None, ""):
                    price = float(override)
                else:
                    price = max(7.0, min(13.0, base + cum))
                current_prices[name] = price

            # Weeks for 3-week rolling
            weeks = [current_gw - 2, current_gw - 1, current_gw]
            weeks = [w for w in weeks if w >= 1]

            # Class 3-week average
            class_vals = []
            for w in weeks:
                for name in raw_data:
                    s = raw_data[name].get(w)
                    if s is not None and s != "":
                        class_vals.append(s)
            class_avg_3w = sum(class_vals) / len(class_vals) if class_vals else 0
            print(f"  Class 3-week average: {class_avg_3w:.1f}%")

            # Compute deltas
            deltas = {}
            for pp_row, name in player_list:
                p_scores = []
                for w in weeks:
                    s = raw_data.get(name, {}).get(w)
                    if s is not None and s != "":
                        p_scores.append(s)
                if not p_scores:
                    deltas[name] = 0.0
                    continue
                p_avg = sum(p_scores) / len(p_scores)
                gap = p_avg - class_avg_3w
                raw_d = get_delta(gap)
                price = current_prices.get(name, 10.0)
                mult = get_multiplier(price)
                adj = raw_d * mult
                adj = max(-0.5, min(0.5, adj))
                deltas[name] = round_tenth(adj)

            # Write deltas to log
            gw_col_log = 2 + current_gw
            for i, (pp_row, name) in enumerate(player_list):
                log_row = pl_data_start + i
                d = deltas[name]
                c = settings.cell(log_row, gw_col_log)
                c.value = d
                c.number_format = '+£0.0"m";-£0.0"m";—'

            # Fix Cumulative formula
            last_col = chr(ord('C') + TOTAL_WEEKS - 1)
            for i, (pp_row, name) in enumerate(player_list):
                log_row = pl_data_start + i
                settings.cell(pp_row, 4, f"=SUM(C{log_row}:{last_col}{log_row})")

            print(f"[OK] Price deltas written to GW{current_gw} log column")
            movers = sorted(deltas.items(), key=lambda x: -abs(x[1]))[:5]
            print("  Top movers:")
            for name, d in movers:
                sign = "+" if d > 0 else ("-" if d < 0 else " ")
                print(f"    {name}: {sign}£{abs(d):.1f}m")

    # =====================================================
    # Bump gameweek
    # =====================================================
    home["C7"] = next_gw
    print(f"[OK] Gameweek advanced: {current_gw} -> {next_gw}")

    # =====================================================
    # Clear TEST RESULTS
    # =====================================================
    for r in range(5, 30):
        if results.cell(r, 2).value is None:
            break
        results.cell(r, 3, None)
    print(f"[OK] TEST RESULTS cleared")

    # =====================================================
    # Save
    # =====================================================
    wb.save(FILE_PATH)
    print(f"[OK] Saved: {FILE_PATH}")
    print()
    print("=" * 62)
    print("DONE")
    print("=" * 62)


if __name__ == "__main__":
    main()