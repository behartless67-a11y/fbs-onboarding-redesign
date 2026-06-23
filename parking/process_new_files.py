import pandas as pd
import re

def fix_capitalization(name):
    """Fix all-caps or improper capitalization."""
    if pd.isna(name) or name == '':
        return name
    name = str(name).strip()
    if name.isupper() or name.islower():
        return name.title()
    return name

def parse_name(full_name, default_last_name=''):
    """Parse a full name into first and last name."""
    if pd.isna(full_name) or full_name == '':
        return None, None, False
    full_name = str(full_name).strip()

    # Remove relationship suffixes
    full_name = re.split(r'\s*[-–—]\s*(?:son|daughter|grandson|granddaughter|parent|mother|father|sister|brother|friend|guest)\s*$', full_name, flags=re.IGNORECASE)[0]
    full_name = re.sub(r'\s*\([^)]*(?:son|daughter|grandson|granddaughter|parent|mother|father|sister|brother|friend|guest)[^)]*\)\s*$', '', full_name, flags=re.IGNORECASE)
    full_name = full_name.strip()

    parts = full_name.split()
    if len(parts) == 0:
        return None, None, False
    elif len(parts) == 1:
        return fix_capitalization(parts[0]), fix_capitalization(default_last_name) if default_last_name else default_last_name, True
    else:
        first_name = ' '.join([fix_capitalization(p) for p in parts[:-1]])
        last_name = fix_capitalization(parts[-1])
        return first_name, last_name, False

def parse_guests_string(guests_str):
    """Parse a comma/newline-separated string of guest names."""
    if pd.isna(guests_str) or guests_str == '':
        return []
    guests_str = str(guests_str)
    # Replace 'and' with comma, split by commas and newlines
    guests_str = re.sub(r'\s+and\s+', ', ', guests_str)
    guests_str = re.sub(r'\n+', ', ', guests_str)
    names = [name.strip() for name in guests_str.split(',')]
    return [name for name in names if name and len(name) > 1]

def text_to_number(text):
    """Convert spelled-out numbers to integers."""
    if pd.isna(text):
        return 0
    text = str(text).lower().strip()

    # Extract numbers from patterns like "Two Passes", "One Pass", etc.
    word_to_num = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
    }

    for word, num in word_to_num.items():
        if word in text:
            return num

    # Try to extract numeric value
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    return 0

# Storage for records
culbreth_records = []
carrs_hill_records = []

# 1. PROCESS BOV PARTICIPATION MATRIX for Culbreth
print("Processing BOV Participation Matrix...")
bov_df = pd.read_excel('C:/Users/Ben/Downloads/BOV_Participation_Matrix_2026.xlsx',
                        sheet_name='Participation Matrix', header=0)

for idx, row in bov_df.iterrows():
    if idx == 0:  # Skip header row
        continue

    last_name = row.get('Unnamed: 1', '')
    status = row.get('Unnamed: 2', '')
    guest_names_str = row.get('Unnamed: 10', '')

    if pd.isna(last_name) or last_name == '' or status == 'Not participating':
        continue

    # Parse guest names
    guest_names = parse_guests_string(guest_names_str)

    for guest_name in guest_names:
        # Check if it's a day-specific note
        if 'saturday' in guest_name.lower() or 'sunday' in guest_name.lower() or 'valedictory' in guest_name.lower():
            continue

        first, last, used_default = parse_name(guest_name, default_last_name=last_name)
        if first:
            culbreth_records.append({
                'Last Name': last if last else last_name,
                'First Name': first,
                'Affiliation': 'BOV',
                'Ceremony Day': 'Both',
                'Number of Passes': 1,
                'Notes': ''
            })

print(f"  Added {len(culbreth_records)} BOV guests")

# 2. PROCESS CREDENTIALS MASTER LIST for Culbreth
print("\nProcessing Credentials Master List...")
creds_df = pd.read_excel('C:/Users/Ben/Downloads/Credentials Master List -  2026 Final Exercises as of 4.30.2026.xlsx')

for idx, row in creds_df.iterrows():
    first_name = fix_capitalization(row.get('First Name', ''))
    last_name = fix_capitalization(row.get('Last Name', ''))
    department = row.get('Department', '')
    title = row.get('Title', '')

    # Check Culbreth parking
    culbreth_passes = row.get('Culbreth Garage / \nJPJ Garage', 0)
    try:
        culbreth_passes = float(culbreth_passes) if pd.notna(culbreth_passes) else 0
    except:
        culbreth_passes = 0

    if culbreth_passes <= 0:
        continue

    # Use department or title as affiliation
    if pd.notna(department) and department != '':
        affiliation = str(department).strip()
    elif pd.notna(title) and title != '':
        affiliation = str(title).strip()
    else:
        affiliation = 'Special Guest'

    culbreth_records.append({
        'Last Name': last_name,
        'First Name': first_name,
        'Affiliation': affiliation,
        'Ceremony Day': 'Both',
        'Number of Passes': int(culbreth_passes),
        'Notes': ''
    })

print(f"  Added {len(culbreth_records) - len([r for r in culbreth_records if r['Affiliation'] == 'BOV'])} from Credentials Master List")

# 3. PROCESS PLATFORM & PROCESSION PARTY for Carr's Hill
print("\nProcessing Platform & Procession Party...")
platform_df = pd.read_excel('C:/Users/Ben/Downloads/Finals Weekend 2026 - Platform & Procession Party_4.15.2026.xlsx')

for idx, row in platform_df.iterrows():
    first_name = fix_capitalization(row.get('First Name:', ''))
    last_name = fix_capitalization(row.get('Last Name:', ''))
    title = row.get('Title and School or Department:', '')

    # Check Saturday passes
    sat_passes_text = row.get('Seating passes \nSaturday, May 16th', '')
    sat_passes = text_to_number(sat_passes_text)
    sat_guests = row.get('Names', '')

    # Check Sunday passes
    sun_passes_text = row.get('Seating passes \nSunday, May 17th', '')
    sun_passes = text_to_number(sun_passes_text)
    sun_guests = row.get('Names.1', '')

    if pd.isna(last_name) or last_name == '':
        continue

    affiliation = str(title).strip() if pd.notna(title) and title != '' else 'Platform Party'

    # Add main person for Saturday
    if sat_passes > 0:
        carrs_hill_records.append({
            'Last Name': last_name,
            'First Name': first_name,
            'Affiliation': affiliation,
            'Ceremony Day': 'Saturday',
            'Number of Passes': sat_passes,
            'Notes': ''
        })

        # Add Saturday guests
        sat_guest_names = parse_guests_string(sat_guests)
        for guest_name in sat_guest_names:
            g_first, g_last, used_default = parse_name(guest_name, default_last_name=last_name)
            if g_first:
                carrs_hill_records.append({
                    'Last Name': g_last if g_last else last_name,
                    'First Name': g_first,
                    'Affiliation': 'Platform Party Guest',
                    'Ceremony Day': 'Saturday',
                    'Number of Passes': 0,
                    'Notes': ''
                })

    # Add main person for Sunday
    if sun_passes > 0:
        carrs_hill_records.append({
            'Last Name': last_name,
            'First Name': first_name,
            'Affiliation': affiliation,
            'Ceremony Day': 'Sunday',
            'Number of Passes': sun_passes,
            'Notes': ''
        })

        # Add Sunday guests
        sun_guest_names = parse_guests_string(sun_guests)
        for guest_name in sun_guest_names:
            g_first, g_last, used_default = parse_name(guest_name, default_last_name=last_name)
            if g_first:
                carrs_hill_records.append({
                    'Last Name': g_last if g_last else last_name,
                    'First Name': g_first,
                    'Affiliation': 'Platform Party Guest',
                    'Ceremony Day': 'Sunday',
                    'Number of Passes': 0,
                    'Notes': ''
                })

print(f"  Added {len(carrs_hill_records)} Platform Party people")

# Save to CSV for now
df_culbreth_new = pd.DataFrame(culbreth_records)
df_carrs_hill = pd.DataFrame(carrs_hill_records)

df_culbreth_new.to_csv('C:/Users/Ben/Downloads/culbreth_new_records.csv', index=False)
df_carrs_hill.to_csv('C:/Users/Ben/Downloads/carrs_hill_records.csv', index=False)

print(f"\nTotal new records:")
print(f"  Culbreth: {len(culbreth_records)}")
print(f"  Carr's Hill: {len(carrs_hill_records)}")
print("\nSaved temporary files for review")
