<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
</head>
<body>
    <h2>Overview</h2>
    <p>NETRECON is a sophisticated Python-based tool designed for ethical network reconnaissance and analysis. Tailored for network administrators, security professionals, and authorized users, it provides robust capabilities to track phone numbers, IP addresses, and scan network ports. The tool features a visually appealing command-line interface with ANSI-colored outputs, progress animations, and interactive HTML map generation. With built-in search history management and a focus on responsible use, NETRECON ensures precise and efficient analysis while adhering to legal and ethical standards.</p>
    <h2>Features</h2>
    <ul>
        <li><strong>Phone Number Tracking</strong>: Retrieves region, carrier, country code, timezone, and generates interactive geolocation maps.</li>
        <li><strong>IP Address Tracking</strong>: Provides detailed location, ISP, and organization information via the ip-api.com service.</li>
        <li><strong>Port Scanning</strong>: Supports quick scans for common ports, full scans (ports 1-1024), or custom port ranges.</li>
        <li><strong>Search History</strong>: Maintains a record of up to 50 recent searches in a JSON file for efficient review.</li>
        <li><strong>Interactive Maps</strong>: Creates HTML-based maps with markers, popups, and approximate coverage areas using Folium.</li>
        <li><strong>User Interface</strong>: Offers a professional CLI with colored outputs, progress bars, and animated banners for enhanced usability.</li>
    </ul>
    <h2>Prerequisites</h2>
    <p>NETRECON requires Python 3.6 or higher and the following libraries:</p>
    <ul>
        <li><code>phonenumbers</code>: For parsing and analyzing Hawkins: For parsing and analyzing phone numbers.</li>
        <li><code>geopy</code>: For geocoding location data.</li>
        <li><code>folium</code>: For generating interactive maps.</li>
        <li><code>requests</code>: For HTTP requests to external APIs.</li>
        <li>Standard Python libraries: <code>uuid</code>, <code>json</code>, <code>socket</code>, <code>threading</code>, <code>datetime</code>.</li>
    </ul>
    <p>Install dependencies using pip:</p>
    <pre><code>pip install phonenumbers geopy folium requests</code></pre>
    <h2>Installation</h2>
    <ol>
        <li>Clone or download the repository containing <code>hell_scanner.py</code>.</li>
        <li>Install the required dependencies (see Prerequisites).</li>
        <li>Run the script:
            <pre><code>python hell_scanner.py</code></pre>
        </li>
    </ol>
    <h2>Usage</h2>
    <ol>
        <li>Launch the script to access the main menu, displayed with an animated banner.</li>
        <li>Select an option (0-5):
            <ul>
                <li><strong>1. Track Phone Number</strong>: Enter a phone number with country code (e.g., <code>+12025551234</code>) to view details and generate a map.</li>
                <li><strong>2. Track IP Address</strong>: Input an IP address or domain to retrieve location and ISP details.</li>
                <li><strong>3. Scan Ports</strong>: Scan an IP address for open ports (quick, full, or custom range).</li>
                <li><strong>4. View History</strong>: Review previously tracked phone numbers and IP addresses.</li>
                <li><strong>5. About</strong>: Display tool information and dependencies.</li>
                <li><strong>0. Exit</strong>: Terminate the program.</li>
            </ul>
        </li>
        <li>Follow on-screen prompts; use <code>q</code> to return to the main menu where applicable.</li>
    </ol>
    <h2>Example</h2>
    <h3>Track a Phone Number</h3>
    <ul>
        <li>Select option <code>1</code>.</li>
        <li>Enter <code>+12025551234</code>.</li>
        <li>View details (region, carrier, timezone) and an interactive map saved as <code>phone_location_YYYYMMDD_HHMMSS.html</code>.</li>
    </ul>
    <h3>Scan Ports</h3>
    <ul>
        <li>Select option <code>3</code>.</li>
        <li>Enter <code>192.168.1.1</code>.</li>
        <li>Choose scan type (e.g., quick) to identify open ports, such as HTTP (port 80).</li>
    </ul>
    <h2>Output Files</h2>
    <ul>
        <li><strong>Maps</strong>: Interactive maps saved as <code>phone_location_YYYYMMDD_HHMMSS.html</code> in the script directory.</li>
        <li><strong>History</strong>: Search history stored in <code>network_tracker_history.json</code>, limited to 50 entries.</li>
    </ul>
    <h2>Ethical and Legal Considerations</h2>
    <div class="warning">
        <ul>
            <li><strong>Responsible Use</strong>: Use NETRECON only on phone numbers, IP addresses, or networks you own or have explicit permission to analyze.</li>
            <li><strong>Legal Compliance</strong>: Unauthorized scanning or tracking may violate local laws or terms of service. Ensure compliance with all applicable regulations.</li>
            <li><strong>Privacy</strong>: Respect the privacy of individuals and organizations when using this tool.</li>
        </ul>
    </div>
    <h2>Limitations</h2>
    <ul>
        <li>Phone number location data is approximate, based on region or country information.</li>
        <li>IP tracking depends on the ip-api.com service, which may have rate limits or inaccuracies.</li>
        <li>Port scanning performance varies with network conditions and firewall configurations.</li>
        <li>An internet connection is required for geolocation, IP tracking, and map generation.</li>
    </ul>
    <h2>Troubleshooting</h2>
    <ul>
        <li><strong>Module Not Found</strong>: Ensure dependencies are installed using <code>pip install phonenumbers geopy folium requests</code>.</li>
        <li><strong>Invalid Phone Number</strong>: Include the country code (e.g., <code>+12025551234</code>).</li>
        <li><strong>Connection Errors</strong>: Verify internet connectivity for API-dependent features.</li>
        <li><strong>Map Not Opening</strong>: Manually open the generated HTML file in a browser if automatic opening fails.</li>
    </ul>
    <h2>Contributing</h2>
    <ol>
        <li>Fork the repository.</li>
        <li>Create a feature branch: <code>git checkout -b feature/new-feature</code>.</li>
        <li>Commit changes: <code>git commit -m "Add new feature"</code>.</li>
        <li>Push to the branch: <code>git push origin feature/new-feature</code>.</li>
        <li>Submit a pull request with a detailed description of your changes.</li>
    </ol>
    <h2>License</h2>
    <p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>
    <h2>Author</h2>
    <p><strong>Zero</strong>: Creator of NETRECON.</p>
    <h2>Disclaimer</h2>
    <p>NETRECON is provided "as is" without warranties. The author is not responsible for any misuse or damage caused by this tool. Use it responsibly and at your own risk.</p>

</body>
</html>
