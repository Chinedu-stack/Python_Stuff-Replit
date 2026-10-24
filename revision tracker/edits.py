import xlwings as xw
import shutil, os
from datetime import date, datetime

# ---------- CONFIG ----------
WB_PATH = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\Revision_Tracker.xlsx"
DASHBOARD = "Dashboard"

# Today's Focus Layout
FOCUS_SUBJECT_ROW = 27          
FOCUS_BOX_ROWS    = [27, 28]    
SESSION_COLS      = ["A", "C", "E", "G"]   

# Colors
GREEN = (217, 234, 211)
RED   = (244, 204, 204)
WHITE = (255, 255, 255)
# ----------------------------

def backup(path):
    folder, name = os.path.split(path)
    stem, ext = os.path.splitext(name)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dst = os.path.join(folder, f"{stem}_BACKUP_{stamp}{ext}")
    shutil.copy2(path, dst)
    print(f"✅ Backup written: {dst}\n")

def last_revised_date(wb, subject):
    """Look at the subject tab and return the max date in Column D."""
    try:
        sheet = wb.sheets[subject]
    except Exception:
        return None

    last_row = sheet.range("A" + str(sheet.cells.last_cell.row)).end("up").row
    if last_row < 4:
        return None

    dates = sheet.range(f"D4:D{last_row}").value
    if not isinstance(dates, list):
        dates = [dates]

    real_dates = []
    for d in dates:
        if isinstance(d, datetime):
            real_dates.append(d.date())
        elif isinstance(d, date):
            real_dates.append(d)
        elif isinstance(d, str) and d.strip():
            for fmt in ("%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d"):
                try:
                    real_dates.append(datetime.strptime(d.strip(), fmt).date())
                    break
                except ValueError:
                    pass
                    
    return max(real_dates) if real_dates else None

def paint_box(sheet, rows, col_letter, color):
    """Color the 2x2 grid solidly without messing up borders."""
    right_col = chr(ord(col_letter) + 1)
    top = rows[0]
    bot = rows[-1]
    
    # Color every cell in the 2x2 block solidly
    for r in rows:
        for c in (col_letter, right_col):
            sheet.range(f"{c}{r}").color = color

def main():
    backup(WB_PATH)

    wb = xw.Book(WB_PATH)
    dash = wb.sheets[DASHBOARD]
    today = date.today()

    print(f"Painting Today's Focus...\n")
    
    for col in SESSION_COLS:
        raw = dash.range(f"{col}{FOCUS_SUBJECT_ROW}").value
        subject = str(raw).strip() if raw else ""

        if not subject or subject == "-":
            paint_box(dash, FOCUS_BOX_ROWS, col, WHITE)
            print(f"  {col}: (blank) -> WHITE")
            continue

        last_date = last_revised_date(wb, subject)

        if last_date == today:
            color, tag = GREEN, "GREEN"
        elif last_date is None:
            color, tag = RED, "RED (no dates)"
        else:
            color, tag = RED, f"RED ({last_date.strftime('%d/%m/%Y')})"

        paint_box(dash, FOCUS_BOX_ROWS, col, color)
        print(f"  {col}: {subject:<25} -> {tag}")

    wb.save()
    print("\nSaved successfully.")

if __name__ == "__main__":
    main()