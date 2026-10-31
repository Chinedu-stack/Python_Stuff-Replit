import xlwings as xw
import json
import datetime
import os

PATH = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\Revision_Tracker.xlsx"
OUTPUT_FILE = r"C:\Users\chine\OneDrive\Python Stuff\revision tracker\extracted_data.json"

# The 10 subjects we want to extract
SUBJECTS = [
    "Biology", "Chemistry", "Physics", "Mathematics",
    "English Language", "English Literature", "Geography",
    "History", "Spanish", "Computer Science"
]

print("Opening Excel to extract data...")
app = xw.App(visible=False, add_book=False)
app.display_alerts = False
app.screen_updating = False

# We need a helper to convert Python dates to JSON-friendly strings
def parse_date(val):
    if isinstance(val, (datetime.date, datetime.datetime)):
        return val.strftime("%Y-%m-%d")
    elif isinstance(val, str) and val.strip() != "":
        return val.strip()
    return None

data_export = {"subjects": []}

try:
    wb = app.books.open(PATH)
    
    for sub_name in SUBJECTS:
        ws = wb.sheets[sub_name]
        
        # 1. Get the General Notes for the Subject (from the merged/unmerged F4:F18 box)
        subject_notes = ws.range("F4").value
        if subject_notes is None:
            subject_notes = ""
            
        subject_data = {
            "subject_name": sub_name,
            "general_notes": str(subject_notes).strip(),
            "topics": []
        }
        
        print(f"Scanning {sub_name}...")
        
        # 2. Loop through the rows to get topics (Rows 4 to 50)
        for r in range(4, 50):
            topic_name = ws.range(f"A{r}").value
            
            # If column A is empty, we've reached the end of the topics for this subject
            if not topic_name:
                continue
                
            status = ws.range(f"B{r}").value
            confidence = ws.range(f"C{r}").value
            last_revised = parse_date(ws.range(f"D{r}").value)
            next_action = ws.range(f"E{r}").value
            
            topic_data = {
                "name": str(topic_name).strip(),
                "status": str(status).strip() if status else "Not Started",
                "confidence": str(confidence).strip() if confidence else None,
                "last_revised": last_revised,
                "next_action": str(next_action).strip() if next_action else None
            }
            
            subject_data["topics"].append(topic_data)
            
        data_export["subjects"].append(subject_data)

    # 3. Save to JSON
    print("Saving to JSON file...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_export, f, indent=4)
        
    print(f"Success! Data extracted to: {OUTPUT_FILE}")
    
    wb.close()

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    app.quit()