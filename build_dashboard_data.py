"""
Build consolidated competitor data for dashboard
Reads from scraped data files and creates docs/data/competitors.json
"""
import json
import os
from datetime import datetime
from pathlib import Path

# Create output directory if needed
output_dir = Path("docs/data")
output_dir.mkdir(parents=True, exist_ok=True)

# Load competitor info from CSV
import csv
competitors_info = {}
with open('competitors.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = f"{row['market'].lower()}_{row['name'].lower().replace(' ', '_')}"
        competitors_info[key] = row

# Build consolidated data
data = {
    'timestamp': datetime.utcnow().isoformat(),
    'competitors': {
        'moldova': [],
        'georgia': [],
        'armenia': []
    }
}

# Process each market
markets = ['moldova', 'georgia', 'armenia']
for market in markets:
    market_data = []

    # Load website monitoring data
    website_file = Path(f"data/websites/changes_{datetime.now().strftime('%Y-%m-%d')}.json")
    website_changes = {}
    if website_file.exists():
        with open(website_file) as f:
            try:
                website_changes = json.load(f)
            except:
                pass

    # Load Facebook data
    fb_file = Path(f"data/facebook/{datetime.now().strftime('%Y-%m-%d')}_{market}.json")
    fb_data = {}
    if fb_file.exists():
        with open(fb_file) as f:
            try:
                fb_data = json.load(f)
            except:
                pass

    # Load Instagram data
    ig_file = Path(f"data/instagram/{datetime.now().strftime('%Y-%m-%d')}_{market}.json")
    ig_data = {}
    if ig_file.exists():
        with open(ig_file) as f:
            try:
                ig_data = json.load(f)
            except:
                pass

    # Get competitors for this market from CSV
    with open('competitors.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['market'].lower() != market:
                continue

            comp_entry = {
                'name': row['name'],
                'market': row['market'],
                'website': row['website_url'],
                'facebook': row['facebook_url'],
                'instagram': row['instagram_handle'],
                'status': 'online',  # Default to online
                'last_updated': datetime.utcnow().isoformat(),
                'prices_found': []
            }

            # Check website status
            if website_changes and 'changes' in website_changes:
                for change in website_changes.get('changes', []):
                    if row['name'].lower() in change.get('competitor', '').lower():
                        if change.get('status') == 'offline':
                            comp_entry['status'] = 'offline'

            market_data.append(comp_entry)

    data['competitors'][market] = market_data

# Write consolidated data
output_file = output_dir / "competitors.json"
with open(output_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✓ Dashboard data saved to {output_file}")
print(f"  - Moldova: {len(data['competitors']['moldova'])} competitors")
print(f"  - Georgia: {len(data['competitors']['georgia'])} competitors")
print(f"  - Armenia: {len(data['competitors']['armenia'])} competitors")
