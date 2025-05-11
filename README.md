Hell Scanner
Overview
Hell Scanner is an advanced network reconnaissance tool designed for tracking phone numbers, IP addresses, and scanning ports. Built with Python, it offers a user-friendly CLI for ethical use by network administrators or security professionals with permission to analyze targets.
Features

Phone Number Tracking: Retrieves region, carrier, country code, timezone, and creates interactive geolocation maps.
IP Address Tracking: Provides location, ISP, and organization details via ip-api.com.
Port Scanning: Scans for open ports (quick, full, or custom ranges).
Search History: Stores up to 50 recent searches in a JSON file.
Interactive Maps: Generates HTML maps with markers and coverage areas.
CLI Interface: Includes ANSI-colored outputs, progress bars, and animated banners.

Prerequisites

Python 3.6+
Required libraries:pip install phonenumbers geopy folium requests



Installation

Clone or download the script (hell_scanner.py).
Install dependencies (see Prerequisites).
Run the script:python hell_scanner.py



Usage

Launch the script to view the main menu.
Choose an option:
1: Track phone number (e.g., +12025551234).
2: Track IP address or domain.
3: Scan ports on an IP address.
4: View search history.
5: About the tool.
0: Exit.


Follow prompts; use q to return to the menu.

Example

Phone Tracking: Enter +12025551234 to see details and a map (phone_location_YYYYMMDD_HHMMSS.html).
Port Scan: Scan 192.168.1.1 for open ports (e.g., HTTP on port 80).

Output Files

Maps: Saved as phone_location_YYYYMMDD_HHMMSS.html.
History: Stored in network_tracker_history.json.

Ethical Considerations

Use only on authorized targets.
Comply with local laws and regulations.
Respect privacy.

Limitations

Approximate phone number locations.
IP tracking depends on ip-api.com accuracy.
Port scanning speed varies by network.
Requires internet for some features.

Troubleshooting

Module Errors: Install dependencies.
Phone Number Issues: Use country code (e.g., +1).
Connection Errors: Verify internet access.
Map Issues: Open HTML files manually if browser fails.

Contributing

Fork the repository.
Create a branch (git checkout -b feature/new).
Commit changes (git commit -m "Add feature").
Push (git push origin feature/new).
Submit a pull request.

License
MIT License (see LICENSE file).
Author

Zero

Disclaimer
Provided "as is." The author is not liable for misuse. Use responsibly.
