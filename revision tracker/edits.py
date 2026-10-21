import xlwings as xw
import shutil
import os

PATH = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\Revision_Tracker.xlsx"

if not os.path.exists(PATH):
    print(f"ERROR: Cannot find {PATH}. Please make sure the file is back in the folder!")
    exit()

print("Opening Excel...")
app = xw.App(visible=False, add_book=False)
app.display_alerts = False
app.screen_updating = False

SUBJECTS = [
    "Biology", "Chemistry", "Physics", "Mathematics",
    "English Language", "English Literature", "Geography",
    "History", "Spanish", "Computer Science"
]

def rgb(r, g, b):
    return b * 65536 + g * 256 + r

try:
    wb = app.books.open(PATH)
    
    c_header = rgb(31, 78, 120)   # Dark blue
    c_white = rgb(255, 255, 255)  # White
    c_border = rgb(189, 215, 238) # Light blue gridline
    
    for sheet_name in SUBJECTS:
        print(f"Creating General Notes on {sheet_name}...")
        ws = wb.sheets[sheet_name]
        
        # 1. Setup Header (Row 3)
        header_cell = ws.range("F3")
        header_cell.value = "General Notes"
        header_cell.api.Interior.Color = c_header
        header_cell.api.Font.Color = rgb(255, 255, 255)
        header_cell.api.Font.Bold = True
        header_cell.api.HorizontalAlignment = -4108
        header_cell.api.VerticalAlignment = -4108
        
        # 2. Setup Big Box (Rows 4 to 18) WITHOUT merging
        for r in range(4, 19):
            cell = ws.range(f"F{r}")
            cell.api.Interior.Color = c_white
            
            # Draw borders around every cell to create one seamless box
            for border_idx in [7, 8, 9, 10]: # Left, Top, Bottom, Right
                cell.api.Borders(border_idx).LineStyle = 1
                cell.api.Borders(border_idx).Color = c_border
                
            # Formatting
            cell.api.WrapText = True
            cell.api.VerticalAlignment = -4160 # Top align
            cell.api.Font.Color = rgb(0, 0, 0)
            
        # 3. Widen the column
        ws.range("F:F").column_width = 55

    wb.save()
    wb.close()
    print("Success! The General Notes column is perfectly formatted.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    app.quit()