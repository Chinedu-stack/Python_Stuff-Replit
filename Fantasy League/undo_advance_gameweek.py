# =========================================================
# undo_advance.py — reverse the last advance
# Only undoes the MOST RECENT gameweek. Restores the archive,
# clears POINTS HISTORY + price log column, decrements GW.
# Note: TEST RESULTS inputs are NOT restored (they were cleared
# on advance). Re-enter them manually if you need them.
# =========================================================
import os
import sys
import glob
import shutil
import logging
from datetime import datetime

import openpyxl
from openpyxl.utils import coordinate_to_tuple, get_column_letter

# =========================================================
# CONFIG
# =========================================================
FILE_PATH  = r"C:\Users\chine\OneDrive\Copies School Fantasy League for editing\11O Fantasy League.xlsx"
BACKUP_DIR = r"C:\Users\chine\OneDrive\Copies School Fantasy League for editing"
PASSWORD   = "Legendx24j@"
BACKUPS_TO_KEEP = 20
LOG_PATH   = os.path.join(BACKUP_DIR, "fantasy_patch.log")

AUTO_CONFIRM = "--yes" in sys.argv or "-y" in sys.argv

RR_SHEET   = "RAW RESULTS"
RR_NAME_C  = 2
RR_FIRST   = 3

PH_SHEET   = "POINTS HISTORY"
PH_NAME_C  = 2
PH_GW1_C   = 3

# =========================================================
# LOGGING
# =========================================================
logging.basicConfig(
    filename=LOG_PATH, level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("undo")
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
    return max(start, r - 1)

def col_for_gw(gw):
    return 2 + gw

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
    if name not in wb.defined_names: return None
    ref = wb.defined_names[name].attr_text
    if "!" not in ref: return None
    sheet, cell = ref.split("!", 1)
    sheet = sheet.strip("'"); cell = cell.replace("$", "")
    r, c = coordinate_to_tuple(cell)
    return sheet, r, c

def read_named(wb, name, default=None):
    info = named_cell(wb, name)
    if not info: return default
    sheet, r, c = info
    if sheet not in wb.sheetnames: return default
    v = wb[sheet].cell(r, c).value
    return v if v not in (None, "") else default

def write_named(wb, name, value):
    info = named_cell(wb, name)
    if not info:
        raise RuntimeError(f"Named range {name} not found")
    sheet, r, c = info
    ws = wb[sheet]
    was = ws.protection.sheet
    if was: ws.protection.sheet = False
    ws.cell(r, c, value)
    if was:
        ws.protection.sheet = True
        ws.protection.password = PASSWORD

# =========================================================
# MAIN
# =========================================================
def main():
    log.info("=" * 62)
    log.info("UNDO ADVANCE")
    log.info("=" * 62)

    if not os.path.exists(FILE_PATH):
        raise FileNotFoundError(FILE_PATH)

    wb = openpyxl.load_workbook(FILE_PATH)
    current_gw = int(read_named(wb, "CurrentGW", 1) or 1)

    if current_gw <= 1:
        log.error("Current GW is %d — nothing to undo.", current_gw)
        return

    target_gw = current_gw - 1
    log.info("Will undo GW%d and return to GW%d.", target_gw, target_gw)

    if not AUTO_CONFIRM:
        print()
        resp = input(f"Undo GW{target_gw}? [Y/N]: ").strip().upper()
        if resp != "Y":
            print("Cancelled.")
            return

    backup = make_backup()
    log.info("[OK] Backup: %s", os.path.basename(backup))

    try:
        raw      = wb[RR_SHEET]
        ph       = wb[PH_SHEET]
        settings = wb["SETTINGS"]

        gw_col = col_for_gw(target_gw)

        # ---- 1. Clear RAW RESULTS GW column ----
        rr_last = last_row(raw, RR_NAME_C, start=RR_FIRST)
        rr_cleared = 0
        for r in range(RR_FIRST, rr_last + 1):
            if raw.cell(r, gw_col).value not in (None, ""):
                rr_cleared += 1
            raw.cell(r, gw_col, None)
        log.info("[OK] Cleared %d cells in RAW RESULTS GW%d",
                 rr_cleared, target_gw)

        # ---- 2. Clear POINTS HISTORY GW column ----
        ph_last = last_row(ph, PH_NAME_C, start=2)
        ph_cleared = 0
        for r in range(2, ph_last + 1):
            if ph.cell(r, gw_col).value not in (None, ""):
                ph_cleared += 1
            ph.cell(r, gw_col, None)
        log.info("[OK] Cleared %d cells in POINTS HISTORY GW%d",
                 ph_cleared, target_gw)

        # ---- 3. Clear price log GW column ----
        pp_hdr = pl_hdr = None
        for r in range(1, 300):
            v = settings.cell(r, 2).value
            if v == "PLAYER PRICES":
                pp_hdr = r + 1
            if isinstance(v, str) and v.startswith("WEEKLY PRICE LOG"):
                pl_hdr = r + 1

        if pp_hdr and pl_hdr:
            pl_start = pl_hdr + 1
            pl_cleared = 0
            for i, r in enumerate(range(pl_start, pl_start + 500)):
                pp_row = pp_hdr + 1 + i
                if settings.cell(pp_row, 2).value is None:
                    break
                if settings.cell(r, gw_col).value not in (None, ""):
                    pl_cleared += 1
                settings.cell(r, gw_col, None)
            log.info("[OK] Cleared %d price deltas for GW%d",
                     pl_cleared, target_gw)
        else:
            log.warning("Could not find price sections — skipped.")

        # ---- 4. Decrement GW ----
        write_named(wb, "CurrentGW", target_gw)
        log.info("[OK] GW reverted to %d", target_gw)

        # ---- 5. Save ----
        wb.save(FILE_PATH)
        prune_backups()
        log.info("[OK] Saved: %s", FILE_PATH)
        log.info("=" * 62)
        log.info("DONE. Back at GW%d.", target_gw)
        log.info("NOTE: TEST RESULTS inputs were cleared by the advance.")
        log.info("      Re-enter them manually if you need them.")

    except Exception:
        log.exception("Undo failed — restoring backup")
        try:
            shutil.copy2(backup, FILE_PATH)
            log.info("[OK] Rolled back from %s", os.path.basename(backup))
        except Exception:
            log.exception("Rollback ALSO failed — manual recovery required")
        raise


if __name__ == "__main__":
    main()