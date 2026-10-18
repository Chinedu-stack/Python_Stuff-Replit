import xlwings as xw
import shutil

PATH = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\Revision_Tracker.xlsx"
BACKUP_PATH = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\Revision_Tracker_BACKUP_BORDERS.xlsx"

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
    
    print("Fixing borders on the Subject column...")
    
    # Target the whole table from Subject header (A13) down to Computer Science (A23)
    # We apply thin grey borders to put the grid lines back
    table_col = ws.range("A13:A23")
    
    # 1. Restore the grey borders
    table_col.api.Borders.LineStyle = 1 # Thin continuous line
    table_col.api.Borders.Color = rgb(220, 220, 220) # Soft grey
    
    # 2. Restore the background colors
    # Row 13 is the header (Needs the soft blue header color)
    ws.range("A13").api.Interior.Color = rgb(207, 226, 243)
    
    # Rows 14-23 are the data (Needs the zebra striping)
    for r in range(14, 24):
        if r % 2 == 0:
            # Even rows get the light grey stripe
            ws.range(f"A{r}").api.Interior.Color = rgb(249, 249, 249)
        else:
            # Odd rows get plain white
            ws.range(f"A{r}").api.Interior.Color = rgb(255, 255, 255)
            
    # Re-center the text just in case
    table_col.api.HorizontalAlignment = -4108 

    wb.save()
    wb.close()
    print("Success! Borders fixed.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    app.quit()