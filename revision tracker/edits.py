import xlwings as xw
import shutil

PATH = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\Revision_Tracker.xlsx"
BACKUP_PATH = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\Revision_Tracker_BACKUP_RESET.xlsx"

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
    ws_dash = wb.sheets["Dashboard"]
    ws_time = wb.sheets["Revision Timetable"]
    
    # ---------------------------------------------------------
    # 1. WIPE EVERYTHING FROM ROW 6 DOWN
    # ---------------------------------------------------------
    print("Wiping old bottom half of Dashboard...")
    # Clear contents and formats from row 6 to the bottom
    ws_dash.range("A6:N100").clear()
    ws_dash.range("A6:N100").api.ClearFormats()
    
    # Colours
    c_header = rgb(207, 226, 243) # Soft blue table header
    c_border = rgb(220, 220, 220) # Table gridlines
    c_focus_bg = rgb(240, 248, 255) # Light blue focus bg
    c_red = rgb(244, 204, 204)    # Soft Red
    c_green = rgb(217, 234, 211)  # Soft Green
    
    # ---------------------------------------------------------
    # 2. BUILD TIMETABLE TAB
    # ---------------------------------------------------------
    print("Building Timetable tab...")
    ws_time.range("A1:Z50").clear()
    ws_time.range("A1:Z50").api.ClearFormats()
    
    week1 = [
        ["Day", "Session 1", "Session 2", "Session 3", "Session 4"],
        ["Monday", "Physics", "English Language", "History", "Spanish"],
        ["Tuesday", "Geography", "Chemistry", "Computer Science", "English Language"],
        ["Wednesday", "Biology", "English Literature", "Mathematics", "Physics"],
        ["Thursday", "English Language", "History", "Biology", "Spanish"],
        ["Friday", "Chemistry", "English Literature", "Computer Science", "Geography"],
        ["Saturday", "Biology", "Mathematics", "-", "-"],
        ["Sunday", "Physics", "English Language", "-", "-"]
    ]
    
    week2 = [
        ["Day", "Session 1", "Session 2", "Session 3", "Session 4"],
        ["Monday", "English Literature", "Physics", "History", "Geography"],
        ["Tuesday", "Biology", "English Language", "Chemistry", "Spanish"],
        ["Wednesday", "Mathematics", "Physics", "English Literature", "Computer Science"],
        ["Thursday", "English Language", "Biology", "Spanish", "Chemistry"],
        ["Friday", "Physics", "History", "English Literature", "English Language"],
        ["Saturday", "Biology", "Geography", "-", "-"],
        ["Sunday", "Mathematics", "Computer Science", "-", "-"]
    ]

    def build_timetable_tab(start_row, start_col, title, data):
        title_cell = ws_time.range((start_row, start_col))
        title_cell.value = title
        title_cell.api.Font.Size = 14
        title_cell.api.Font.Bold = True
        
        for r_idx, row_data in enumerate(data):
            for c_idx, val in enumerate(row_data):
                cell = ws_time.range((start_row + r_idx, start_col + c_idx))
                cell.value = val
                
                # Exact match of your screenshot (soft colors)
                if r_idx == 0:
                    cell.api.Interior.Color = c_header
                    cell.api.Font.Bold = True
                else:
                    if r_idx % 2 == 0:
                        cell.api.Interior.Color = rgb(249, 249, 249)
                    else:
                        cell.api.Interior.Color = rgb(255, 255, 255)
                        
                cell.api.Borders.LineStyle = 1
                cell.api.Borders.Color = c_border
                cell.api.HorizontalAlignment = -4108

    build_timetable_tab(1, 1, "🗓️ Week 1 Timetable", week1)
    build_timetable_tab(1, 7, "🗓️ Week 2 Timetable", week2)
    
    for col in ["A","B","C","D","E","G","H","I","J","K"]:
        ws_time.range(f"{col}:{col}").column_width = 16

    # ---------------------------------------------------------
    # 3. BUILD TODAY'S FOCUS (Rows 8 to 10)
    # ---------------------------------------------------------
    print("Building Today's Focus...")
    ws_dash.range("A8").value = "🎯 Today's Focus"
    ws_dash.range("A8").api.Font.Size = 14
    ws_dash.range("A8").api.Font.Bold = True
    ws_dash.range("A8").api.Font.Color = rgb(31, 78, 120)
    
    sessions = ["Session 1", "Session 2", "Session 3", "Session 4"]
    col_starts = [1, 3, 5, 7] 
    
    for i, session_name in enumerate(sessions):
        c = col_starts[i]
        col_index = i + 1
        
        # Header
        header_cell = ws_dash.range((9, c))
        header_cell.value = session_name
        header_cell.api.Font.Bold = True
        header_cell.api.HorizontalAlignment = -4108
        
        # Formula
        formula_cell = ws_dash.range((10, c))
        formula = (
            f'=IFERROR('
            f'HYPERLINK("#\'"&INDEX(\'Revision Timetable\'!B2:E8, MATCH(TEXT(TODAY(),"dddd"), \'Revision Timetable\'!A2:A8, 0), {col_index})&"\'!A4", '
            f'INDEX(\'Revision Timetable\'!B2:E8, MATCH(TEXT(TODAY(),"dddd"), \'Revision Timetable\'!A2:A8, 0), {col_index})), "-")'
        )
        formula_cell.formula = formula
        
        # Base Styling
        formula_cell.api.Interior.Color = c_focus_bg
        formula_cell.api.Font.Bold = True
        formula_cell.api.Font.Size = 12
        formula_cell.api.Font.Underline = -4142
        formula_cell.api.HorizontalAlignment = -4108
        formula_cell.api.Borders.LineStyle = 1
        formula_cell.api.Borders.Color = c_border
        
    # Merge blocks
    ws_dash.range("A9:B9").api.Merge()
    ws_dash.range("A10:B10").api.Merge()
    ws_dash.range("C9:D9").api.Merge()
    ws_dash.range("C10:D10").api.Merge()
    ws_dash.range("E9:F9").api.Merge()
    ws_dash.range("E10:F10").api.Merge()
    ws_dash.range("G9:H9").api.Merge()
    ws_dash.range("G10:H10").api.Merge()
    
    # ---------------------------------------------------------
    # 4. BUILD PROGRESS BY SUBJECT (Starts at Row 14)
    # ---------------------------------------------------------
    print("Rebuilding Progress by Subject...")
    ws_dash.range("A14").value = "📚 Progress by Subject"
    ws_dash.range("A14").api.Font.Size = 14
    ws_dash.range("A14").api.Font.Bold = True
    ws_dash.range("A14").api.Font.Color = rgb(31, 78, 120)
    
    headers = ["Subject", "Total Topics", "Not Started", "In Progress", "Completed", "Green", "Amber", "Red", "Last Revised"]
    for c_idx, h in enumerate(headers):
        cell = ws_dash.range((15, c_idx + 1))
        cell.value = h
        cell.api.Interior.Color = c_header
        cell.api.Font.Bold = True
        cell.api.HorizontalAlignment = -4108
        cell.api.Borders.LineStyle = 1
        cell.api.Borders.Color = c_border
        
    SUBJECTS = ["Biology", "Chemistry", "Physics", "Mathematics", "English Language", "English Literature", "Geography", "History", "Spanish", "Computer Science"]
    
    for r_idx, sub in enumerate(SUBJECTS):
        r = 16 + r_idx
        sub_cell = ws_dash.range(f"A{r}")
        sub_cell.value = sub
        sub_cell.api.Hyperlinks.Add(Anchor=sub_cell.api, Address="", SubAddress=f"'{sub}'!A4", TextToDisplay=sub)
        sub_cell.api.Font.Bold = True
        sub_cell.api.Font.Underline = -4142
        sub_cell.api.Font.Color = rgb(59, 59, 59)
        
        formulas = [
            f'=SUMPRODUCT(COUNTIFS(INDIRECT("\'{sub}\'!A4:A1000"),"?*"))',
            f'=SUMPRODUCT(COUNTIFS(INDIRECT("\'{sub}\'!A4:A1000"),"?*",INDIRECT("\'{sub}\'!B4:B1000"),"Not Started"))',
            f'=SUMPRODUCT(COUNTIFS(INDIRECT("\'{sub}\'!A4:A1000"),"?*",INDIRECT("\'{sub}\'!B4:B1000"),"In Progress"))',
            f'=SUMPRODUCT(COUNTIFS(INDIRECT("\'{sub}\'!A4:A1000"),"?*",INDIRECT("\'{sub}\'!B4:B1000"),"Completed"))',
            f'=SUMPRODUCT(COUNTIFS(INDIRECT("\'{sub}\'!A4:A1000"),"?*",INDIRECT("\'{sub}\'!C4:C1000"),"Green"))',
            f'=SUMPRODUCT(COUNTIFS(INDIRECT("\'{sub}\'!A4:A1000"),"?*",INDIRECT("\'{sub}\'!C4:C1000"),"Amber"))',
            f'=SUMPRODUCT(COUNTIFS(INDIRECT("\'{sub}\'!A4:A1000"),"?*",INDIRECT("\'{sub}\'!C4:C1000"),"Red"))',
            f'=IF(MAX(\'{sub}\'!D4:D1000)=0, "-", IF(MAX(\'{sub}\'!D4:D1000)=TODAY(), "Today", IF(TODAY()-MAX(\'{sub}\'!D4:D1000)=1, "Yesterday", TODAY()-MAX(\'{sub}\'!D4:D1000) & " days ago")))'
        ]
        
        for c_idx, formula in enumerate(formulas):
            c = c_idx + 2
            cell = ws_dash.range((r, c))
            cell.formula = formula
            cell.api.Borders.LineStyle = 1
            cell.api.Borders.Color = c_border
            cell.api.HorizontalAlignment = -4108
            cell.api.Font.Color = rgb(59, 59, 59)
            if r % 2 == 0:
                cell.api.Interior.Color = rgb(249, 249, 249)
            else:
                cell.api.Interior.Color = rgb(255, 255, 255)
                
        sub_cell.api.Borders.LineStyle = 1
        sub_cell.api.Borders.Color = c_border
        sub_cell.api.HorizontalAlignment = -4108
        if r % 2 == 0:
            sub_cell.api.Interior.Color = rgb(249, 249, 249)
        else:
            sub_cell.api.Interior.Color = rgb(255, 255, 255)

    # ---------------------------------------------------------
    # 5. APPLY RED/GREEN LOGIC TO TODAY'S FOCUS
    # ---------------------------------------------------------
    print("Applying Red/Green logic...")
    focus_boxes = ["A10:B10", "C10:D10", "E10:F10", "G10:H10"]
    for box in focus_boxes:
        rng = ws_dash.range(box)
        rng.api.FormatConditions.Delete()
        # Check against the new table starting at Row 16
        rng.api.FormatConditions.Add(2, None, f'VLOOKUP($A10, $A$16:$I$25, 9, FALSE)<>"Today"').Interior.Color = c_red
        rng.api.FormatConditions.Add(2, None, f'VLOOKUP($A10, $A$16:$I$25, 9, FALSE)="Today"').Interior.Color = c_green
        rng.api.Font.Color = rgb(31, 78, 120)
        rng.api.Font.Bold = True

    # Widths
    ws_dash.range("A:A").column_width = 22
    for col in ["B", "C", "D", "E", "F", "G", "H"]:
        ws_dash.range(f"{col}:{col}").column_width = 14
    ws_dash.range("I:I").column_width = 18

    app.calculate()
    wb.save()
    wb.close()
    print("Success! Dashboard rebuilt flawlessly.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    app.quit()