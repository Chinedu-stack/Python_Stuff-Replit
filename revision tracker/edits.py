import xlwings as xw
import shutil

PATH = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\Revision_Tracker.xlsx"
BACKUP_PATH = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\Revision_Tracker_BACKUP_FINAL_COLORS.xlsx"

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
    
    print("Fixing box structure and applying bulletproof colors...")
    
    c_dark_green = rgb(134, 188, 113) # Strong green
    c_red = rgb(244, 204, 204)        # Soft red
    c_border = rgb(220, 220, 220)     # Border grey
    
    # We target the actual subject cells (A27, C27, E27, G27)
    # and their immediate neighbors so it looks like one big box
    boxes = [
        {"main": "A27", "neighbor": "B27", "hidden": "A28"},
        {"main": "C27", "neighbor": "D27", "hidden": "C28"},
        {"main": "E27", "neighbor": "F27", "hidden": "E28"},
        {"main": "G27", "neighbor": "H27", "hidden": "G28"}
    ]
    
    for box in boxes:
        main = box["main"]
        neighbor = box["neighbor"]
        hidden = box["hidden"]
        
        # 1. UNMERGE the cells so Conditional Formatting actually works
        try:
            ws.range(f"{main}:{neighbor}").api.UnMerge()
        except:
            pass
            
        # 2. Write the hidden helper formula in Row 28
        formula = f'=IF(COUNTIFS($A$13:$A$23, {main}, $I$13:$I$23, "Today")>0, "DONE", "NOT DONE")'
        ws.range(hidden).formula = formula
        ws.range(hidden).api.Font.Color = rgb(255, 255, 255) # Invisible text
        ws.range(hidden).api.Font.Size = 1
        
        # 3. Apply Conditional Formatting to BOTH the main and neighbor cells
        for cell_addr in [main, neighbor]:
            rng = ws.range(cell_addr)
            rng.api.FormatConditions.Delete() # Clear old rules
            
            # Red rule
            rule_red = rng.api.FormatConditions.Add(1, 3, '"NOT DONE"')
            rule_red.Interior.Color = c_red
            rule_red.Font.Color = rgb(150, 0, 0)
            
            # Green rule
            rule_green = rng.api.FormatConditions.Add(1, 3, '"DONE"')
            rule_green.Interior.Color = c_dark_green
            rule_green.Font.Color = rgb(255, 255, 255)
            rule_green.Font.Bold = True
            
            # Draw the borders so it looks like a single box
            for border_idx in [7, 8, 9, 10]:
                rng.api.Borders(border_idx).LineStyle = 1
                rng.api.Borders(border_idx).Color = c_border

    app.calculate()
    wb.save()
    wb.close()
    print("Success! The Focus boxes are unmerged, color-coded, and bulletproof.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    app.quit()