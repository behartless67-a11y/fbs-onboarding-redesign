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

def parse_name_with_suffix(full_name, default_last_name=''):
    """Parse a full name, keeping Jr/Sr/II/III/IV with the last name."""
    if pd.isna(full_name) or full_name == '':
        return None, None, False

    full_name = str(full_name).strip()

    # Remove relationship suffixes (but NOT Jr/Sr/II/III/IV)
    full_name = re.split(r'\s*[-–—]\s*(?:son|daughter|grandson|granddaughter|parent|mother|father|sister|brother|friend|guest)\s*$', full_name, flags=re.IGNORECASE)[0]
    full_name = re.sub(r'\s*\([^)]*(?:son|daughter|grandson|granddaughter|parent|mother|father|sister|brother|friend|guest)[^)]*\)\s*$', '', full_name, flags=re.IGNORECASE)
    full_name = full_name.strip()

    # Remove asterisks and parentheses
    full_name = full_name.replace('*', '')
    full_name = re.sub(r'\([^)]*\)', '', full_name).strip()

    parts = full_name.split()
    if len(parts) == 0:
        return None, None, False
    elif len(parts) == 1:
        return fix_capitalization(parts[0]), fix_capitalization(default_last_name) if default_last_name else default_last_name, True
    else:
        # Check if last part is a suffix (Jr, Sr, II, III, IV, etc.)
        suffix_pattern = r'^(Jr\.?|Sr\.?|II|III|IV|V|2nd|3rd)$'
        has_suffix = len(parts) >= 2 and re.match(suffix_pattern, parts[-1], re.IGNORECASE)

        if has_suffix and len(parts) >= 3:
            # Last name is second-to-last + suffix
            first_name = ' '.join([fix_capitalization(p) for p in parts[:-2]])
            last_name = fix_capitalization(parts[-2]) + ' ' + parts[-1]
            return first_name, last_name, False
        elif has_suffix and len(parts) == 2:
            # Only "FirstName Jr" - use default last name
            first_name = fix_capitalization(parts[0])
            last_name = fix_capitalization(default_last_name) + ' ' + parts[-1] if default_last_name else parts[-1]
            return first_name, last_name, True
        else:
            # Normal case
            first_name = ' '.join([fix_capitalization(p) for p in parts[:-1]])
            last_name = fix_capitalization(parts[-1])
            return first_name, last_name, False

def parse_guests_string(guests_str):
    """Parse a comma/newline-separated string of guest names."""
    if pd.isna(guests_str) or guests_str == '':
        return []
    guests_str = str(guests_str)
    guests_str = re.sub(r'\s+and\s+', ', ', guests_str)
    guests_str = re.sub(r'\n+', ', ', guests_str)
    names = [name.strip() for name in guests_str.split(',')]
    return [name for name in names if name and len(name) > 1]

def text_to_number(text):
    """Convert spelled-out numbers to integers."""
    if pd.isna(text):
        return 0
    text = str(text).lower().strip()
    word_to_num = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
    }
    for word, num in word_to_num.items():
        if word in text:
            return num
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    return 0

# Storage
culbreth_records = []
carrs_hill_records = []

# 1. Load existing Culbreth data (already deduplicated)
print("Loading existing Culbreth data...")
existing = pd.read_excel('C:/Users/Ben/Downloads/Graduation_Parking_Reconciled_2026_v2.xlsx')

# Clean existing data
for idx, row in existing.iterrows():
    # Clean names of asterisks and parentheses
    last_name = str(row['Last Name']).replace('*', '').strip()
    last_name = re.sub(r'\([^)]*\)', '', last_name).strip()
    first_name = str(row['First Name']).replace('*', '').strip()
    first_name = re.sub(r'\([^)]*\)', '', first_name).strip()

    if last_name and last_name != 'nan':
        culbreth_records.append({
            'Last Name': last_name,
            'First Name': first_name,
            'Affiliation': row['Affiliation'],
            'Ceremony Day': row['Ceremony Day'],
            'Number of Passes': row['Number of Passes'],
            'Notes': row.get('Notes', '')
        })

print(f"  Loaded {len(culbreth_records)} existing records")

# 2. Re-process BOV with better name parsing
print("\nRe-processing BOV...")
bov_df = pd.read_excel('C:/Users/Ben/Downloads/BOV_Participation_Matrix_2026.xlsx',
                       sheet_name='Participation Matrix', header=0)

bov_added = 0
for idx, row in bov_df.iterrows():
    if idx == 0:
        continue

    last_name = row.get('Unnamed: 1', '')
    status = row.get('Unnamed: 2', '')
    guest_names_str = row.get('Unnamed: 10', '')

    if pd.isna(last_name) or last_name == '' or status == 'Not participating':
        continue

    guest_names = parse_guests_string(guest_names_str)

    for guest_name in guest_names:
        if 'saturday' in guest_name.lower() or 'sunday' in guest_name.lower() or 'valedictory' in guest_name.lower():
            continue

        first, last, used_default = parse_name_with_suffix(guest_name, default_last_name=last_name)
        if first:
            culbreth_records.append({
                'Last Name': last if last else last_name,
                'First Name': first,
                'Affiliation': 'BOV',
                'Ceremony Day': 'Both',
                'Number of Passes': 1,
                'Notes': ''
            })
            bov_added += 1

print(f"  Added {bov_added} BOV guests")

# 3. Re-process Credentials Master List
print("\nRe-processing Credentials Master List...")
creds_df = pd.read_excel('C:/Users/Ben/Downloads/Credentials Master List -  2026 Final Exercises as of 4.30.2026.xlsx')

creds_added = 0
for idx, row in creds_df.iterrows():
    first_name = fix_capitalization(row.get('First Name', ''))
    last_name = fix_capitalization(row.get('Last Name', ''))
    department = row.get('Department', '')
    title = row.get('Title', '')

    # Clean names
    last_name = last_name.replace('*', '').strip() if pd.notna(last_name) else ''
    first_name = first_name.replace('*', '').strip() if pd.notna(first_name) else ''

    culbreth_passes = row.get('Culbreth Garage / \nJPJ Garage', 0)
    try:
        culbreth_passes = float(culbreth_passes) if pd.notna(culbreth_passes) else 0
    except:
        culbreth_passes = 0

    if culbreth_passes <= 0:
        continue

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
    creds_added += 1

print(f"  Added {creds_added} from Credentials")

# 4. Re-process Platform & Procession
print("\nRe-processing Platform & Procession...")
platform_df = pd.read_excel('C:/Users/Ben/Downloads/Finals Weekend 2026 - Platform & Procession Party_4.15.2026.xlsx')

for idx, row in platform_df.iterrows():
    first_name = fix_capitalization(row.get('First Name:', ''))
    last_name = fix_capitalization(row.get('Last Name:', ''))
    title = row.get('Title and School or Department:', '')

    sat_passes_text = row.get('Seating passes \nSaturday, May 16th', '')
    sat_passes = text_to_number(sat_passes_text)
    sat_guests = row.get('Names', '')

    sun_passes_text = row.get('Seating passes \nSunday, May 17th', '')
    sun_passes = text_to_number(sun_passes_text)
    sun_guests = row.get('Names.1', '')

    if pd.isna(last_name) or last_name == '':
        continue

    affiliation = str(title).strip() if pd.notna(title) and title != '' else 'Platform Party'

    if sat_passes > 0:
        carrs_hill_records.append({
            'Last Name': last_name,
            'First Name': first_name,
            'Affiliation': affiliation,
            'Ceremony Day': 'Saturday',
            'Number of Passes': sat_passes,
            'Notes': ''
        })

        sat_guest_names = parse_guests_string(sat_guests)
        for guest_name in sat_guest_names:
            g_first, g_last, used_default = parse_name_with_suffix(guest_name, default_last_name=last_name)
            if g_first:
                carrs_hill_records.append({
                    'Last Name': g_last if g_last else last_name,
                    'First Name': g_first,
                    'Affiliation': 'Platform Party Guest',
                    'Ceremony Day': 'Saturday',
                    'Number of Passes': 0,
                    'Notes': ''
                })

    if sun_passes > 0:
        carrs_hill_records.append({
            'Last Name': last_name,
            'First Name': first_name,
            'Affiliation': affiliation,
            'Ceremony Day': 'Sunday',
            'Number of Passes': sun_passes,
            'Notes': ''
        })

        sun_guest_names = parse_guests_string(sun_guests)
        for guest_name in sun_guest_names:
            g_first, g_last, used_default = parse_name_with_suffix(guest_name, default_last_name=last_name)
            if g_first:
                carrs_hill_records.append({
                    'Last Name': g_last if g_last else last_name,
                    'First Name': g_first,
                    'Affiliation': 'Platform Party Guest',
                    'Ceremony Day': 'Sunday',
                    'Number of Passes': 0,
                    'Notes': ''
                })

print(f"  Added {len(carrs_hill_records)} Platform Party")

# Deduplicate
def affiliation_priority(affiliation):
    return 0 if affiliation == 'Special Guest' else 1

df_culbreth = pd.DataFrame(culbreth_records)
df_culbreth['affiliation_priority'] = df_culbreth['Affiliation'].apply(affiliation_priority)
df_culbreth = df_culbreth.sort_values(
    by=['Last Name', 'First Name', 'affiliation_priority', 'Number of Passes'],
    ascending=[True, True, False, False]
)
df_culbreth = df_culbreth.drop_duplicates(subset=['Last Name', 'First Name'], keep='first')
df_culbreth = df_culbreth.drop(columns=['affiliation_priority'])
df_culbreth = df_culbreth.sort_values(by=['Last Name', 'First Name'])

df_carrs = pd.DataFrame(carrs_hill_records)
df_carrs['affiliation_priority'] = df_carrs['Affiliation'].apply(affiliation_priority)
df_carrs = df_carrs.sort_values(
    by=['Last Name', 'First Name', 'affiliation_priority', 'Number of Passes'],
    ascending=[True, True, False, False]
)
df_carrs = df_carrs.drop_duplicates(subset=['Last Name', 'First Name'], keep='first')
df_carrs = df_carrs.drop(columns=['affiliation_priority'])
df_carrs = df_carrs.sort_values(by=['Last Name', 'First Name'])

# Save
with pd.ExcelWriter('C:/Users/Ben/Downloads/Graduation_Parking_Reconciled_2026_Final.xlsx', engine='openpyxl') as writer:
    df_culbreth.to_excel(writer, sheet_name='Culbreth Garage', index=False)
    df_carrs.to_excel(writer, sheet_name='Carrs Hill Madison Hall', index=False)

print(f"\nFinal counts:")
print(f"  Culbreth: {len(df_culbreth)}")
print(f"  Carrs Hill: {len(df_carrs)}")
