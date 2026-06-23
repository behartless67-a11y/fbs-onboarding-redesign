import pandas as pd
import re

def clean_name(name):
    """Remove asterisks, parentheses, and other weird characters from names."""
    if pd.isna(name) or name == '':
        return name
    name = str(name).strip()
    # Remove asterisks
    name = name.replace('*', '')
    # Remove parentheses and their contents
    name = re.sub(r'\([^)]*\)', '', name)
    name = name.strip()
    return name

# Read both tabs
culbreth = pd.read_excel('C:/Users/Ben/Downloads/Graduation_Parking_Reconciled_2026_Final.xlsx',
                         sheet_name='Culbreth Garage')
carrs_hill = pd.read_excel('C:/Users/Ben/Downloads/Graduation_Parking_Reconciled_2026_Final.xlsx',
                           sheet_name='Carrs Hill Madison Hall')

print("Fixing Culbreth data...")

# Clean names
culbreth['Last Name'] = culbreth['Last Name'].apply(clean_name)
culbreth['First Name'] = culbreth['First Name'].apply(clean_name)

# Remove rows where last name is empty after cleaning
culbreth = culbreth[culbreth['Last Name'].notna() & (culbreth['Last Name'] != '')]

# Fix specific known issues
# "Jr" and "Sr" should be part of first name, not last name
problematic_last_names = ['Jr', 'Sr', 'Jr.', 'Sr.']
for idx, row in culbreth.iterrows():
    if row['Last Name'] in problematic_last_names:
        # This is wrong - need to look at original data to fix properly
        print(f"  WARNING: Found '{row['Last Name']}' as last name for {row['First Name']}")

print(f"Culbreth after cleaning: {len(culbreth)} records")

print("\nFixing Carr's Hill data...")
carrs_hill['Last Name'] = carrs_hill['Last Name'].apply(clean_name)
carrs_hill['First Name'] = carrs_hill['First Name'].apply(clean_name)
carrs_hill = carrs_hill[carrs_hill['Last Name'].notna() & (carrs_hill['Last Name'] != '')]

print(f"Carr's Hill after cleaning: {len(carrs_hill)} records")

# Re-check Platform & Procession to make sure we got everyone
print("\n" + "="*80)
print("VERIFYING PLATFORM & PROCESSION PARSING:")
print("="*80)

platform = pd.read_excel('C:/Users/Ben/Downloads/Finals Weekend 2026 - Platform & Procession Party_4.15.2026.xlsx')

# Show who has passes
print("\nPeople with SATURDAY passes:")
sat_people = platform[platform['Seating passes \nSaturday, May 16th'].notna()]
for idx, row in sat_people.iterrows():
    print(f"  {row['First Name:']} {row['Last Name:']} - {row['Seating passes \nSaturday, May 16th']}")

print("\nPeople with SUNDAY passes:")
sun_people = platform[platform['Seating passes \nSunday, May 17th'].notna()]
for idx, row in sun_people.iterrows():
    print(f"  {row['First Name:']} {row['Last Name:']} - {row['Seating passes \nSunday, May 17th']}")

# Save cleaned version
with pd.ExcelWriter('C:/Users/Ben/Downloads/Graduation_Parking_Reconciled_2026_Final.xlsx', engine='openpyxl') as writer:
    culbreth.to_excel(writer, sheet_name='Culbreth Garage', index=False)
    carrs_hill.to_excel(writer, sheet_name='Carrs Hill Madison Hall', index=False)

print(f"\n✓ Cleaned Excel saved")
print(f"  Culbreth: {len(culbreth)} records")
print(f"  Carr's Hill: {len(carrs_hill)} records")
