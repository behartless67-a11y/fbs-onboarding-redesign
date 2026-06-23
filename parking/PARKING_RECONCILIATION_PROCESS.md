# Graduation Parking Reconciliation Process

## Overview
This document explains how to reconcile multiple parking spreadsheets into a single master list for Parking & Transportation.

## Input Files Required

1. **Finals Weekend Parking List (MASTER) 2026.xlsx**
   - Use the specific tab: `CH&MH, Culbreth, JPJ. Sat & Sun` (or whichever location you're processing)
   - Contains staff/crew parking by date

2. **Ceremony Files** (4 files total):
   - `Saturday (2)_4.28.2026.xlsx` - Saturday 2pm ceremony guests
   - `Saturday (4)_4.28.2026.xlsx` - Saturday 4pm ceremony guests
   - `Sunday (2)_4.28.2026.xlsx` - Sunday 2pm ceremony guests
   - `Sunday (4)_4.28.2026.xlsx` - Sunday 4pm ceremony guests

3. **Faculty Marshals 2026_List for Parking.xlsx**
   - Contains faculty marshal names (first and last name only)

## Key Processing Rules

### Red Text Exclusion
- **Any row with red text is from last year and should be excluded**
- Red text detection looks for RGB color `FFFF0000` (pure red)
- This applies to ALL input files

### Name Parsing Rules
1. **All-caps names** are converted to Title Case for readability
2. **First name only** (no last name provided): Use the family's last name
3. **Names in message/notes fields**: Extract and add to the list
4. **Relationship suffixes removed**: Strip "- granddaughter", "- son", etc. from names
5. **Summary rows excluded**: Skip any rows with last name "Total", "Subtotal", "Grand Total"

### Affiliation Assignment
- Staff/crew from MASTER: "Special Guest"
- Ceremony guests: "Special Guest"
- Graduating students: "Special Guest"
- Faculty marshals: "Faculty Marshal"

### Ceremony Day Assignment
- Staff/crew: "Saturday" or "Sunday" (based on which day they need parking)
- Ceremony guests: "Saturday" or "Sunday" (based on their ceremony)
- Faculty marshals: "Both" (need parking both days)

### Guest Parsing
From ceremony files, extract and create individual rows for:
1. **Main contact person** (Last Name, First Name columns) - gets parking pass count
2. **Graduating student** (from "Please enter the graduating students' name:" column) - 0 passes
3. **Guests** (from "Guests" column, comma-separated) - 0 passes each
4. **Additional names in messages** (from "Message to the Event Coordinator" column) - 0 passes each

### Notes Column (Excel only)
- "Last name inferred from family" - when only first name was provided
- "From message field" - when name was extracted from notes/messages
- **Notes column is NOT included in Word document**

## Output Files

### 1. Excel Spreadsheet
**File**: `Graduation_Parking_Reconciled_2026_v2.xlsx`

**Columns**:
- Last Name (first column)
- First Name
- Affiliation
- Ceremony Day
- Number of Passes
- Notes

**Format**:
- Sorted alphabetically by Last Name, then First Name
- One person per row
- All names in Title Case (not ALL CAPS)

### 2. Word Document
**File**: `Parking_List_2026_Final.docx`

**Format**:
- Title: "Special Guest & Faculty Marshal Parking List"
- Date headers: "Final Exercises – 2026" and ceremony dates
- Table with columns: Day, Location, First Name, Last Name, Affiliation, Spaces/Notes
- Margins: 0.5 inches all around
- Font: 9pt for data, 10pt for headers
- Spaces/Notes column: Only shows parking pass numbers (no text notes)

**Key Differences from Excel**:
- Location column shows parking location (e.g., "Culbreth")
- NO Notes column text (only pass numbers)
- Formatted for printing/distribution

## How to Run for a Different Location

### Step 1: Update the Python Script

Open `reconcile_parking.py` and modify these sections:

#### Change the MASTER file tab:
```python
# Line ~133
sheet_name = 'CH&MH, Culbreth, JPJ. Sat & Sun'  # CHANGE THIS
```

#### Update the output file names:
```python
# Line ~226
output_file = 'C:/Users/Ben/Downloads/Graduation_Parking_Reconciled_2026_v2.xlsx'
```

Change to something like:
```python
output_file = 'C:/Users/Ben/Downloads/JPJ_Parking_Reconciled_2026.xlsx'
```

### Step 2: Run the Excel Generation
```bash
python "c:\Users\Ben\Desktop\AI_Projects\sandbox\reconcile_parking.py"
```

This creates the Excel file with all reconciled data.

### Step 3: Generate the Word Document

Create a separate Python script or modify the existing one to generate the Word doc:

```python
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import pandas as pd

# Read the reconciled Excel file
df = pd.read_excel('C:/Users/Ben/Downloads/YOUR_EXCEL_FILE.xlsx')

# Create Word doc (same code as before)
doc = Document()

# Set margins
sections = doc.sections
for section in sections:
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

# Add title and headers...
# (See full code in reconcile_parking.py)

# IMPORTANT: Change the location name
row_cells[1].text = "YOUR LOCATION NAME HERE"  # e.g., "JPJ", "Culbreth", etc.
```

### Step 4: Verify Output

#### Excel Checklist:
- [ ] No "Total" summary rows
- [ ] No red text entries (last year's data)
- [ ] All names in Title Case (not ALL CAPS)
- [ ] Sorted alphabetically by Last Name
- [ ] Notes column shows inferred last names

#### Word Document Checklist:
- [ ] Correct location name in every row
- [ ] No text notes (only parking pass numbers)
- [ ] "Faculty Marshal" and "Special Guest" fit on one line
- [ ] No text wrapping issues
- [ ] All names in Title Case

### Step 5: Spot Check

Pick a few last names and verify:
1. All family members are included
2. Graduating student is listed
3. Names from "Guests" column are split into individual rows
4. Names from message field are included
5. Last names are correct (especially for first-name-only entries)

## Common Issues & Solutions

### Issue: "Permission denied" when saving Excel file
**Solution**: Close the Excel file if it's open

### Issue: Names still in ALL CAPS
**Solution**: The `fix_capitalization()` function should handle this. Check that it's being called for all name fields.

### Issue: Missing people
**Solution**: Check if they have red text in the original file (means last year's data)

### Issue: "Total" rows appearing
**Solution**: The script filters for last names "total", "subtotal", "grand total" (case-insensitive)

### Issue: Wrong graduating student last name
**Solution**: Script infers last name from family. If wrong, manually fix in Excel output.

### Issue: Names like "Elizabeth (Ellie) Smith - granddaughter"
**Solution**: Script removes relationship suffixes. Check the regex patterns in `parse_name()` function.

## Files Location

- **Python Script**: `c:\Users\Ben\Desktop\AI_Projects\sandbox\reconcile_parking.py`
- **Input Files**: `C:/Users/Ben/Downloads/`
- **Output Files**: `C:/Users/Ben/Downloads/`

## Processing Summary

For the Culbreth location (May 2026):
- **Input**: 5 files (1 MASTER tab, 4 ceremony files, 1 faculty marshal file)
- **Red text excluded**: 603 rows from MASTER, 1 from Saturday 2pm, 0 from others
- **Output**: 904 records total
  - 211 Faculty Marshals (with "Both" ceremony day)
  - 693 Special Guests (Saturday or Sunday)
- **Excel file**: Includes Notes column
- **Word file**: No Notes column, shows only parking pass numbers

## Contact

If you need to modify the script or have questions about the process:
- Python script location: `c:\Users\Ben\Desktop\AI_Projects\sandbox\reconcile_parking.py`
- This documentation: `c:\Users\Ben\Desktop\AI_Projects\sandbox\PARKING_RECONCILIATION_PROCESS.md`
