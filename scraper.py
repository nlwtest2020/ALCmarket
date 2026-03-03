#!/usr/bin/env python3
import json
import urllib.request
from datetime import datetime
from html.parser import HTMLParser
import re

class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            attrs_dict = dict(attrs)
            if 'property' in attrs_dict and 'content' in attrs_dict:
                self.data[attrs_dict['property']] = attrs_dict['content']
            elif 'name' in attrs_dict and 'content' in attrs_dict:
                self.data[attrs_dict['name']] = attrs_dict['content']

def scrape_url(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            html = response.read().decode('utf-8', errors='ignore')
        return html
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_metadata(html):
    parser = MetaParser()
    parser.feed(html)
    return parser.data

def extract_price_info(html):
    prices = re.findall(r'\$\d+[\d,]*|\€\d+[\d,]*|\d+\s*(lei|MDL|GEL|AMD)', html, re.IGNORECASE)
    return prices[:5] if prices else []

def track_competitor(name, website, facebook_url=None, instagram_handle=None):
    competitor = {
        'name': name,
        'website': website,
        'last_updated': datetime.utcnow().isoformat(),
        'status': 'offline'
    }

    if not website:
        return competitor

    # Try to fetch website
    html = scrape_url(website)
    if html:
        competitor['status'] = 'online'
        meta = extract_metadata(html)
        competitor['metadata'] = meta
        competitor['prices_found'] = extract_price_info(html)

        # Extract title
        title_match = re.search(r'<title>([^<]+)</title>', html)
        if title_match:
            competitor['title'] = title_match.group(1)

    if facebook_url:
        competitor['facebook'] = facebook_url
    if instagram_handle:
        competitor['instagram'] = instagram_handle

    return competitor

# Hardcoded real competitor data
COMPETITORS = {
    'moldova': [
        {'name': 'Top English', 'website': 'https://www.topenglishtv.md/', 'country': 'Moldova'},
        {'name': 'Linguata', 'website': 'https://linguata.md/', 'country': 'Moldova'},
        {'name': 'Oratorica', 'website': 'https://oratorica.md/', 'country': 'Moldova'},
        {'name': 'Engleza cu Snow', 'website': 'https://englezacusnow.md/', 'country': 'Moldova'},
        {'name': 'Alliance Francaise', 'website': 'https://alliancefr.md/', 'country': 'Moldova'},
        {'name': 'ILTC', 'website': 'https://iltc.md/', 'country': 'Moldova'},
        {'name': 'Lingua Franca', 'website': 'https://linguafranca.md/', 'country': 'Moldova'},
        {'name': 'Terra Nova', 'website': 'https://terranova.md/', 'country': 'Moldova'},
        {'name': 'Quo Vadis', 'website': 'https://quovadis.md/', 'country': 'Moldova'},
        {'name': 'Art House', 'website': 'https://arthouse.md/', 'country': 'Moldova'},
        {'name': 'Fantastic', 'website': 'https://fantastic.md/', 'country': 'Moldova'},
        {'name': 'Smile English', 'website': 'https://smileenglish.md/', 'country': 'Moldova'},
    ],
    'georgia': [
        {'name': 'British Council Tbilisi', 'website': 'https://www.britishcouncil.ge/', 'country': 'Georgia'},
        {'name': 'International House Tbilisi', 'website': 'https://ih.ge/', 'country': 'Georgia'},
        {'name': 'Goethe-Institut Georgia', 'website': 'https://www.goethe.de/ge/', 'country': 'Georgia'},
        {'name': 'Institut français de Géorgie', 'website': 'https://www.ifgeorgia.ge/', 'country': 'Georgia'},
        {'name': 'Beka\'s School', 'website': 'https://bekasschool.ge/', 'country': 'Georgia'},
        {'name': 'Levels Academy', 'website': 'https://levelsacademy.ge/', 'country': 'Georgia'},
        {'name': 'EMCAN', 'website': 'https://emcan.ge/', 'country': 'Georgia'},
        {'name': 'English Skills', 'website': 'https://englishskills.ge/', 'country': 'Georgia'},
        {'name': 'British Centre Georgia', 'website': 'https://britishcentre.ge/', 'country': 'Georgia'},
        {'name': 'Goga Askurava School', 'website': 'https://gogaaskurava.ge/', 'country': 'Georgia'},
        {'name': 'TCS', 'website': 'https://tcs.ge/', 'country': 'Georgia'},
        {'name': 'Sepia', 'website': 'https://sepia.ge/', 'country': 'Georgia'},
    ],
    'armenia': [
        {'name': 'ICLT', 'website': 'https://iclt.am/', 'country': 'Armenia'},
        {'name': 'Berlitz Yerevan', 'website': 'https://www.berlitz.am/', 'country': 'Armenia'},
        {'name': '42 Yerevan', 'website': 'https://42yerevan.am/', 'country': 'Armenia'},
        {'name': 'BDG Language Center', 'website': 'https://bdg.am/', 'country': 'Armenia'},
        {'name': 'AUA', 'website': 'https://aua.am/', 'country': 'Armenia'},
    ]
}

def main():
    all_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'competitors': {}
    }

    for market, competitors in COMPETITORS.items():
        all_data['competitors'][market] = []
        for comp in competitors:
            tracked = track_competitor(
                comp['name'],
                comp['website']
            )
            tracked['country'] = comp['country']
            tracked['market'] = market
            all_data['competitors'][market].append(tracked)
            print(f"✓ {comp['name']} - {tracked['status']}")

    # Save to docs/data/
    with open('docs/data/competitors.json', 'w') as f:
        json.dump(all_data, f, indent=2)

    print(f"\n✓ Data saved to docs/data/competitors.json")
    print(f"✓ Total competitors tracked: {sum(len(c) for c in all_data['competitors'].values())}")

if __name__ == '__main__':
    main()
