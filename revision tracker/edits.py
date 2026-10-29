import xlwings as xw
import shutil

PATH = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\Revision_Tracker.xlsx"
BACKUP_PATH = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\Revision_Tracker_BACKUP_RAG.xlsx"

print("Creating backup...")
shutil.copy2(PATH, BACKUP_PATH)

print("Opening Excel...")
app = xw.App(visible=False, add_book=False)
app.display_alerts = False
app.screen_updating = False

def rgb(r, g, b):
    return b * 65536 + g * 256 + r

try:
    wb = app.books.open(PATH)
    ws = wb.sheets["Dashboard"]
    
    print("Fixing the RAG tile formulas...")
    
    # The tiles are in Row 9. 
    # Green is A9:B9
    # Amber is C9:D9
    # Red is E9:F9
    
    # 1. Green Formula
    # This SUMPRODUCT formula counts all "Green" in column C of every subject sheet.
    formula_green = '=SUMPRODUCT(COUNTIFS(INDIRECT("\'"&Subjects&"\'!A4:A1000"),"?*",INDIRECT("\'"&Subjects&"\'!C4:C1000"),"Green"))'
    ws.range("A9").formula = formula_green
    ws.range("A9").number_format = "General"
    
    # 2. Amber Formula
    formula_amber = '=SUMPRODUCT(COUNTIFS(INDIRECT("\'"&Subjects&"\'!A4:A1000"),"?*",INDIRECT("\'"&Subjects&"\'!C4:C1000"),"Amber"))'
    ws.range("C9").formula = formula_amber
    ws.range("C9").number_format = "General"
    
    # 3. Red Formula
    formula_red = '=SUMPRODUCT(COUNTIFS(INDIRECT("\'"&Subjects&"\'!A4:A1000"),"?*",INDIRECT("\'"&Subjects&"\'!C4:C1000"),"Red"))'
    ws.range("E9").formula = formula_red
    ws.range("E9").number_format = "General"

    app.calculate()
    wb.save()
    wb.close()
    print("Success! RAG numbers fixed.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    app.quit()