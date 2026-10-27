import xlwings as xw

PATH = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\Revision_Tracker.xlsx"

print("Opening Excel...")
app = xw.App(visible=False, add_book=False)
app.display_alerts = False
app.screen_updating = False

def rgb(r, g, b):
    return b * 65536 + g * 256 + r

try:
    wb = app.books.open(PATH)
    ws = wb.sheets["Dashboard"]
    
    print("Adding Week Toggle and updating formulas...")
    
    # 1. Setup the Toggle in A24 (just above Today's Focus)
    ws.range("A24").value = "Current Week:"
    ws.range("A24").api.Font.Bold = True
    ws.range("A24").api.Font.Color = rgb(31, 78, 120)
    
    toggle_cell = ws.range("B24")
    toggle_cell.value = 2 # Default to Week 2 right now
    toggle_cell.api.HorizontalAlignment = -4108 # Center
    
    # Style the toggle box
    toggle_cell.api.Interior.Color = rgb(207, 226, 243) # Soft blue
    toggle_cell.api.Font.Bold = True
    
    # Add Dropdown (1 or 2) to B24
    try:
        toggle_cell.api.Validation.Delete()
        toggle_cell.api.Validation.Add(3, 1, 1, "1,2") # 3 = xlValidateList
    except: pass

    # 2. Update the Today's Focus Formulas
    # We assume the Focus subject boxes are at A27, C27, E27, G27
    # (If they moved, this script might need to be adjusted, but based on our last screenshot they are at 27)
    
    start_row = 27
    sessions = ["Session 1", "Session 2", "Session 3", "Session 4"]
    col_starts = [1, 3, 5, 7] # A, C, E, G
    
    for i, session_name in enumerate(sessions):
        c = col_starts[i]
        col_index = i + 1
        
        formula_cell = ws.range((start_row, c))
        
        # The Magic Dynamic Formula
        # It looks at $B$24. If 1 -> INDEX/Range A2:E8. If 2 -> INDEX/Range G2:K8.
        formula = (
            f'=IFERROR('
            f'HYPERLINK("#\'"&INDEX(IF($B$24=1, \'Revision Timetable\'!B2:E8, \'Revision Timetable\'!H2:K8), MATCH(TEXT(TODAY(),"dddd"), \'Revision Timetable\'!A2:A8, 0), {col_index})&"\'!A4", '
            f'INDEX(IF($B$24=1, \'Revision Timetable\'!B2:E8, \'Revision Timetable\'!H2:K8), MATCH(TEXT(TODAY(),"dddd"), \'Revision Timetable\'!A2:A8, 0), {col_index})), "-")'
        )
        
        formula_cell.formula = formula

    app.calculate()
    wb.save()
    wb.close()
    print("Success! Week Toggle added. You can now switch between Week 1 and 2.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    app.quit()