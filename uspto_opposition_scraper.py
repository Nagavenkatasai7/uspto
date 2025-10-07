#!/usr/bin/env python3
"""
USPTO Opposition Trademark Scraper
Retrieves US and International classes from serial numbers in opposition pleaded applications.
"""

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from typing import List, Dict, Set
import sys
import time


class USPTOOppositionScraper:
    """Scraper for USPTO opposition trademark data."""

    def __init__(self, api_key: str):
        """
        Initialize scraper with API key.

        Args:
            api_key: USPTO API key for TSDR access
        """
        self.api_key = api_key
        self.tsdr_base_url = "https://tsdrapi.uspto.gov/ts/cd/casestatus/sn{}/info.json"
        self.ttabvue_base_url = "https://ttabvue.uspto.gov/ttabvue/v"
        self.session = requests.Session()
        self.session.headers.update({'USPTO-API-KEY': self.api_key})

    def get_serial_numbers_from_opposition(self, opposition_number: str) -> List[Dict[str, str]]:
        """
        Scrape TTABVue to get serial numbers from pleaded applications section.

        Args:
            opposition_number: Opposition number (e.g., "91302017")

        Returns:
            List of dicts with serial_number and mark_name
        """
        print(f"[1/4] Fetching opposition {opposition_number} from TTABVue...")

        params = {
            'pno': opposition_number,
            'pty': 'OPP'
        }

        try:
            response = requests.get(self.ttabvue_base_url, params=params, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching TTABVue page: {e}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the "Pleaded applications and registrations" section
        serial_numbers = []

        # Look for the table containing pleaded applications
        # The structure may vary, so we'll search for serial number patterns
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            # Serial numbers appear in TSDR links
            if 'tsdr.uspto.gov' in href or 'sn=' in href:
                # Extract serial number from various formats
                if 'sn=' in href:
                    sn = href.split('sn=')[1].split('&')[0]
                    mark_name = link.get_text(strip=True)
                    serial_numbers.append({
                        'serial_number': sn,
                        'mark_name': mark_name
                    })

        # Alternative: Look for serial numbers in table cells
        if not serial_numbers:
            # Find tables and search for 8-digit numbers (serial number pattern)
            import re
            serial_pattern = re.compile(r'\b\d{8}\b')

            for table in soup.find_all('table'):
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    for cell in cells:
                        text = cell.get_text(strip=True)
                        match = serial_pattern.search(text)
                        if match:
                            sn = match.group(0)
                            # Try to find mark name in adjacent cells
                            mark_name = ''
                            next_cell = cell.find_next_sibling(['td', 'th'])
                            if next_cell:
                                mark_name = next_cell.get_text(strip=True)

                            serial_numbers.append({
                                'serial_number': sn,
                                'mark_name': mark_name or 'Unknown'
                            })

        # Remove duplicates while preserving order
        seen = set()
        unique_serials = []
        for item in serial_numbers:
            sn = item['serial_number']
            if sn not in seen:
                seen.add(sn)
                unique_serials.append(item)

        if not unique_serials:
            print("❌ No serial numbers found in pleaded applications section.")
            return []

        print(f"✓ Found {len(unique_serials)} serial numbers in pleaded applications")
        return unique_serials

    def get_classes_from_serial(self, serial_number: str) -> Dict:
        """
        Fetch US and International classes for a serial number via TSDR API.

        Args:
            serial_number: Trademark serial number

        Returns:
            Dict with us_classes, international_classes, and description
        """
        url = self.tsdr_base_url.format(serial_number)

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(f"  ⚠ Error fetching serial {serial_number}: {e}")
            return {
                'us_classes': [],
                'international_classes': [],
                'description': 'Error fetching data'
            }

        # Parse the response
        try:
            trademark = data['trademarks'][0]
            gs_list = trademark.get('gsList', [])

            us_classes = []
            international_classes = []
            descriptions = []

            for gs in gs_list:
                # Get US classes
                for uc in gs.get('usClasses', []):
                    us_classes.append({
                        'code': uc['code'],
                        'description': uc['description']
                    })

                # Get International classes
                for ic in gs.get('internationalClasses', []):
                    international_classes.append({
                        'code': ic['code'],
                        'description': ic['description']
                    })

                # Get description
                desc = gs.get('description', '')
                if desc:
                    descriptions.append(desc)

            return {
                'us_classes': us_classes,
                'international_classes': international_classes,
                'description': ' | '.join(descriptions) if descriptions else ''
            }

        except (KeyError, IndexError) as e:
            print(f"  ⚠ Error parsing data for serial {serial_number}: {e}")
            return {
                'us_classes': [],
                'international_classes': [],
                'description': 'Error parsing data'
            }

    def scrape_opposition(self, opposition_number: str) -> Dict:
        """
        Main method to scrape opposition data.

        Args:
            opposition_number: Opposition number

        Returns:
            Dict with all scraped data
        """
        # Step 1: Get serial numbers
        serials = self.get_serial_numbers_from_opposition(opposition_number)

        if not serials:
            return {
                'opposition_number': opposition_number,
                'serial_count': 0,
                'data': [],
                'unique_us_classes': set(),
                'unique_international_classes': set()
            }

        # Step 2: Fetch class data for each serial number
        print(f"\n[2/4] Fetching class data for {len(serials)} serial numbers...")

        all_data = []
        unique_us_classes = set()
        unique_international_classes = set()

        for idx, serial_info in enumerate(serials, 1):
            sn = serial_info['serial_number']
            mark_name = serial_info['mark_name']

            print(f"  [{idx}/{len(serials)}] Processing {sn} ({mark_name})...")

            class_data = self.get_classes_from_serial(sn)

            # Extract unique class codes
            us_codes = [c['code'] for c in class_data['us_classes']]
            intl_codes = [c['code'] for c in class_data['international_classes']]

            unique_us_classes.update(us_codes)
            unique_international_classes.update(intl_codes)

            all_data.append({
                'serial_number': sn,
                'mark_name': mark_name,
                'us_classes': class_data['us_classes'],
                'international_classes': class_data['international_classes'],
                'us_class_codes': ', '.join(us_codes),
                'international_class_codes': ', '.join(intl_codes),
                'description': class_data['description']
            })

            # Small delay to avoid rate limiting
            time.sleep(0.5)

        print(f"\n✓ Completed data retrieval for all serial numbers")

        return {
            'opposition_number': opposition_number,
            'serial_count': len(serials),
            'data': all_data,
            'unique_us_classes': sorted(unique_us_classes),
            'unique_international_classes': sorted(unique_international_classes)
        }

    def export_to_excel(self, result: Dict, filename: str):
        """Export results to Excel file."""
        print(f"\n[3/4] Exporting to Excel: {filename}")

        if not result['data']:
            print("❌ No data to export")
            return

        # Prepare data for DataFrame
        rows = []
        for item in result['data']:
            rows.append({
                'Opposition Number': result['opposition_number'],
                'Serial Number': item['serial_number'],
                'Mark Name': item['mark_name'],
                'US Classes': item['us_class_codes'],
                'International Classes': item['international_class_codes'],
                'Description': item['description']
            })

        df = pd.DataFrame(rows)

        # Create Excel writer with multiple sheets
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='Trademark Classes', index=False)

            # Summary sheet
            summary_data = {
                'Metric': [
                    'Opposition Number',
                    'Total Serial Numbers',
                    'Unique US Classes',
                    'Unique International Classes'
                ],
                'Value': [
                    result['opposition_number'],
                    result['serial_count'],
                    ', '.join(result['unique_us_classes']),
                    ', '.join(result['unique_international_classes'])
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

        print(f"✓ Excel file created: {filename}")

    def export_to_json(self, result: Dict, filename: str):
        """Export results to JSON file."""
        print(f"\n[4/4] Exporting to JSON: {filename}")

        # Convert sets to lists for JSON serialization
        export_data = {
            'opposition_number': result['opposition_number'],
            'serial_count': result['serial_count'],
            'unique_us_classes': result['unique_us_classes'],
            'unique_international_classes': result['unique_international_classes'],
            'trademarks': result['data']
        }

        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)

        print(f"✓ JSON file created: {filename}")


def main():
    """Main execution function."""
    # Configuration
    API_KEY = "22tljOtfx4tyI7uld3rp2iRqy2UsAvUE"

    # Get opposition number from command line or prompt
    if len(sys.argv) > 1:
        opposition_number = sys.argv[1]
    else:
        opposition_number = input("Enter opposition number: ").strip()

    if not opposition_number:
        print("Error: Opposition number is required")
        sys.exit(1)

    print("=" * 70)
    print("USPTO OPPOSITION TRADEMARK CLASS SCRAPER")
    print("=" * 70)
    print(f"Opposition Number: {opposition_number}\n")

    # Initialize scraper
    scraper = USPTOOppositionScraper(API_KEY)

    # Scrape data
    result = scraper.scrape_opposition(opposition_number)

    if result['serial_count'] == 0:
        print("\n❌ No data found. Please check the opposition number.")
        sys.exit(1)

    # Export results
    excel_filename = f"opposition_{opposition_number}_classes.xlsx"
    json_filename = f"opposition_{opposition_number}_classes.json"

    scraper.export_to_excel(result, excel_filename)
    scraper.export_to_json(result, json_filename)

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Opposition Number: {result['opposition_number']}")
    print(f"Total Serial Numbers: {result['serial_count']}")
    print(f"Unique US Classes: {', '.join(result['unique_us_classes'])}")
    print(f"Unique International Classes: {', '.join(result['unique_international_classes'])}")
    print("=" * 70)
    print("\n✓ Process completed successfully!")


if __name__ == "__main__":
    main()
