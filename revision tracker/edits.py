import xlwings as xw
import shutil

PATH = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\Revision_Tracker.xlsx"
BACKUP_PATH = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\Revision_Tracker_BACKUP_RED.xlsx"

print("Creating backup...")
shutil.copy2(PATH, BACKUP_PATH)

SUBJECTS = [
    "Biology", "Chemistry", "Physics", "Mathematics",
    "English Language", "English Literature", "Geography",
    "History", "Spanish", "Computer Science"
]

print("Opening Excel...")
app = xw.App(visible=False, add_book=False)
app.display_alerts = False
app.screen_updating = False

def rgb(r, g, b):
    return b * 65536 + g * 256 + r

try:
    wb = app.books.open(PATH)
    
    print("Turning 'Return to Dashboard' links red...")
    
    # A nice, soft red that matches the aesthetic
    soft_red = rgb(220, 50, 50) 
    
    for sheet_name in SUBJECTS:
        ws = wb.sheets[sheet_name]
        cell = ws.range("A2")
        
        # Check if the cell has a hyperlink and is the return link
        if cell.api.Hyperlinks.Count > 0:
            cell.api.Font.Color = soft_red
            print(f"  -> Changed color on {sheet_name}")

    wb.save()
    wb.close()
    print("Success! Links are now red.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    app.quit()