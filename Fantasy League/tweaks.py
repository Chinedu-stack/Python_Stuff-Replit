# patch_cumulative.py
import sys, os
from openpyxl import load_workbook

WB_PATH = r"C:\Users\chine\OneDrive\Copies School Fantasy League for editing\11O Fantasy League.xlsx"
SET_PLAYER_START = 22
SET_LOG_START = 55
PLAYER_SLOTS = 30

if not os.path.exists(WB_PATH):
    print(f"ERROR: {WB_PATH} not found"); sys.exit(1)

wb = load_workbook(WB_PATH)
s = wb["SETTINGS"]
n = 0
for i in range(PLAYER_SLOTS):
    pr = SET_PLAYER_START + i   # D row on PLAYER PRICES block
    lr = SET_LOG_START + i      # matching row in WEEKLY PRICE LOG
    s.cell(pr, 4).value = f'=IF(B{pr}="","",SUM(C{lr}:V{lr}))'
    n += 1
print(f"Patched {n} cumulative formulas in SETTINGS!D")
wb.save(WB_PATH)
print("Saved.")