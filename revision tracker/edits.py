import xlwings as xw
import shutil

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
    
    print("Finding the exact table location...")
    table_row = None
    last_rev_col = None
    
    # Find the header row
    for r in range(1, 50):
        for c in range(1, 15):
            val = ws.range((r, c)).value
            if val and "Last Revised" in str(val):
                table_row = r
                last_rev_col = c
                break
        if table_row:
            break
            
    if not table_row:
        print("Could not find the 'Last Revised' column. Exiting.")
    else:
        print(f"Found table at Row {table_row}, Last Revised is Column {last_rev_col}")
        
        # 1. Insert the new column right before 'Last Revised'
        ws.range((table_row, last_rev_col)).api.EntireColumn.Insert(Shift=-4161)
        
        # 2. Set up the Header
        header_cell = ws.range((table_row, last_rev_col))
        header_cell.value = "% Complete"
        
        # Colours matching the rest of the table
        c_header = rgb(207, 226, 243)
        c_zebra = rgb(249, 249, 249)
        c_white = rgb(255, 255, 255)
        c_border = rgb(220, 220, 220)
        
        # 3. Style the Header
        header_cell.api.Interior.Color = c_header
        header_cell.api.Font.Bold = True
        header_cell.api.Font.Name = "Segoe UI"
        header_cell.api.HorizontalAlignment = -4108 # Center
        
        for b_idx in [7, 8, 9, 10]:
            header_cell.api.Borders(b_idx).LineStyle = 1
            header_cell.api.Borders(b_idx).Color = c_border
            
        # 4. Add formulas and styling to the rows
        for r in range(table_row + 1, table_row + 11): # 10 subjects
            cell = ws.range((r, last_rev_col))
            
            # Formula: Completed (Col E) / Total Topics (Col B)
            cell.formula = f"=IFERROR(E{r}/B{r}, 0)"
            cell.number_format = "0%"
            
            # Formatting
            cell.api.Font.Name = "Segoe UI"
            cell.api.HorizontalAlignment = -4108 # Center
            cell.api.Font.Color = rgb(59, 59, 59)
            
            for b_idx in [7, 8, 9, 10]:
                cell.api.Borders(b_idx).LineStyle = 1
                cell.api.Borders(b_idx).Color = c_border
                
            # Zebra stripes
            if r % 2 == 0:
                cell.api.Interior.Color = c_zebra
            else:
                cell.api.Interior.Color = c_white
                
        # 5. Adjust width
        ws.range((table_row, last_rev_col)).api.EntireColumn.ColumnWidth = 14

        app.calculate()
        wb.save()
        print("Success! Percentage column added cleanly without breaking anything.")
        
    wb.close()

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    app.quit()