# patch_market_sort.py
# ONE change only: rewrite PLAYER MARKET rows 5..34 so players are ordered
# by current price (Final from SETTINGS!F) descending, ties broken by SETTINGS row order.
#
# Uses a hidden helper column (G) on the same sheet for the tiebreak key.
# No other sheets touched.

import sys, os
from openpyxl import load_workbook

WB_PATH = r"C:\Users\chine\OneDrive\Copies School Fantasy League for editing\11O Fantasy League.xlsx"
SET_PLAYER_START = 22
PLAYER_SLOTS = 30
PM_START = 5
PM_END = 34

if not os.path.exists(WB_PATH):
    print(f"ERROR: {WB_PATH} not found"); sys.exit(1)

print(f"Opening {WB_PATH}")
wb = load_workbook(WB_PATH)
m = wb["PLAYER MARKET"]

# Ensure the helper column G has a header that's visibly blank-ish
m["G1"] = ""   # nothing in G1; helper occupies G5:G34

for i in range(PLAYER_SLOTS):
    r = PM_START + i
    calc_r = 2 + i          # CALCULATIONS!A2 is first player

    # Helper key in column G:
    # Sort key = Price + tiny row-based tiebreak. We use a large multiplier on price
    # so ties within the same 0.1m band still sort by SETTINGS row order.
    # price * 1000 - row  => strictly descending by price, ascending by row on ties.
    # We invert so LARGE() picks the right thing.
    m.cell(r, 7).value = (
        f'=IF(CALCULATIONS!A{calc_r}="","",'
        f'ROUND(CALCULATIONS!C{calc_r}*1000,0) - {i})'
    )

    # Which rank this row represents (1 = highest price)
    rank = i + 1

    # Price lookup: LARGE of the helper column, Nth = rank
    m.cell(r, 3).value = (
        f'=IFERROR(LARGE($G${PM_START}:$G${PM_END},{rank})/1000,"")'
    )
    m.cell(r, 3).number_format = '£0.0"m"'

    # Player name: find the row whose helper matches this LARGE, then pull CALCULATIONS!A of that row.
    # We need INDEX/MATCH against the helper column, then map back to the player by offset.
    m.cell(r, 2).value = (
        f'=IFERROR(INDEX(CALCULATIONS!$A${2}:$A${1+PLAYER_SLOTS},'
        f'MATCH(LARGE($G${PM_START}:$G${PM_END},{rank}),$G${PM_START}:$G${PM_END},0)),"")'
    )

    # Change: same as before, but driven by the looked-up player name
    m.cell(r, 4).value = (
        f'=IF(B{r}="","",'
        f'IF(CurrentGW<SETTINGS!$C$16,0,'
        f'INDEX(CALCULATIONS!$C${2}:$C${1+PLAYER_SLOTS},MATCH(B{r},CALCULATIONS!$A${2}:$A${1+PLAYER_SLOTS},0))'
        f'-'
        f'INDEX(CALCULATIONS!$B${2}:$B${1+PLAYER_SLOTS},MATCH(B{r},CALCULATIONS!$A${2}:$A${1+PLAYER_SLOTS},0))'
        f'))'
    )
    m.cell(r, 4).number_format = '"▲ +£"0.0"m";"▼ -£"0.0"m";"— £0.0m"'

    # Ownership
    m.cell(r, 5).value = (
        f'=IF(B{r}="","",'
        f'COUNTIF(CALCULATIONS!$L$2:$P${1+PLAYER_SLOTS},B{r})'
        f'/COUNTA(CALCULATIONS!$K$2:$K${1+PLAYER_SLOTS}))'
    )
    m.cell(r, 5).number_format = '0%'

print(f"Rewrote PLAYER MARKET rows {PM_START}..{PM_END} with sort-by-price logic")

# Hide helper column G so students don't see it
m.column_dimensions["G"].hidden = True
m.column_dimensions["G"].width = 6

wb.save(WB_PATH)
print("Saved. Open the workbook to verify.")