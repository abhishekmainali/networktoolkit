import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from geopy.geocoders import Nominatim
import folium
from folium.plugins import Fullscreen, MeasureControl
import os
import sys
import time
import webbrowser
import json
import requests
import socket
import platform
import threading
from datetime import datetime
import uuid

class Colors:
    """ANSI color codes for terminal coloring"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RED = '\033[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRADIENT = [
        '\033[92m',  # Green
        '\033[93m',  # Yellow
        '\033[91m',  # Red
    ]

def clear_screen():
    """Clear the terminal screen based on the operating system"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_banner():
    """Display the custom Hell Scanner ASCII art banner with typing animation"""
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   {Colors.RED}███╗   ██╗███████╗████████╗██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗{Colors.CYAN} ║
║   {Colors.RED}████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║{Colors.CYAN} ║
║   {Colors.RED}██╔██╗ ██║█████╗     ██║   ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║{Colors.CYAN} ║
║   {Colors.RED}██║╚██╗██║██╔══╝     ██║   ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║{Colors.CYAN} ║
║   {Colors.RED}██║ ╚████║███████╗   ██║   ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║{Colors.CYAN} ║
║   {Colors.RED}╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝{Colors.CYAN} ║
║                                                                          ║
║   {Colors.GREEN}Advanced Network Reconnaissance Tool v2.0{Colors.CYAN}                              ║
║   {Colors.WARNING}Created by: ZERO{Colors.CYAN}                                                       ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    for line in banner.split('\n'):
        print(line, flush=True)
        time.sleep(0.05)  # Simulate typing effect
    time.sleep(0.5)

def progress_bar_animation(message, duration=2):
    """Display a progress bar animation for loading"""
    bar_length = 30
    end_time = time.time() + duration
    print(f"\n{message}", end="")
    while time.time() < end_time:
        for i in range(bar_length + 1):
            progress = i / bar_length
            bar = '█' * int(progress * bar_length) + '-' * (bar_length - int(progress * bar_length))
            print(f"\r{message} [{bar}] {int(progress * 100)}%", end="", flush=True)
            time.sleep(duration / (bar_length * 2))
        for i in range(bar_length, -1, -1):
            progress = i / bar_length
            bar = '█' * int(progress * bar_length) + '-' * (bar_length - int(progress * bar_length))
            print(f"\r{message} [{bar}] {int(progress * 100)}%", end="", flush=True)
            time.sleep(duration / (bar_length * 2))
    print("\r" + " " * (len(message) + bar_length + 10), end="\r")

def fade_in_menu(menu_lines):
    """Display menu with a fade-in effect"""
    for line in menu_lines:
        for i in range(1, len(line) + 1):
            print(f"\r{Colors.BLUE}{line[:i]}{Colors.ENDC}", end="", flush=True)
            time.sleep(0.01)
        print()  # Move to next line
        time.sleep(0.1)

class NetworkTracker:
    """Combined Phone Number and IP Tracking Tool"""
    
    def __init__(self):
        self.history = []
        self.load_history()
    
    def load_history(self):
        """Load search history from file if exists"""
        try:
            if os.path.exists("network_tracker_history.json"):
                with open("network_tracker_history.json", "r") as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"{Colors.FAIL}Failed to load history: {e}{Colors.ENDC}")
    
    def save_history(self):
        """Save search history to file"""
        try:
            with open("network_tracker_history.json", "w") as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"{Colors.FAIL}Failed to save history: {e}{Colors.ENDC}")
    
    def get_phone_info(self, phone_number):
        """Extract information from a phone number"""
        try:
            parsed_number = phonenumbers.parse(phone_number)
            if not phonenumbers.is_valid_number(parsed_number):
                return None, "Invalid phone number format."
            
            region = geocoder.description_for_number(parsed_number, "en")
            service_provider = carrier.name_for_number(parsed_number, "en")
            time_zones = timezone.time_zones_for_number(parsed_number)
            country_code = parsed_number.country_code
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            
            data = {
                "type": "phone",
                "formatted_number": formatted_number,
                "country_code": country_code,
                "region": region,
                "carrier": service_provider,
                "timezone": time_zones,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.history.append(data)
            if len(self.history) > 50:
                self.history = self.history[-50:]
            self.save_history()
            
            return data, None
        except Exception as e:
            return None, f"Error processing phone number: {str(e)}"
    
    def get_location_coordinates(self, phone_number):
        """Get approximate coordinates for the phone number's region"""
        try:
            parsed_number = phonenumbers.parse(phone_number)
            region = geocoder.description_for_number(parsed_number, "en")
            country = phonenumbers.region_code_for_number(parsed_number)
            
            query = f"{region}, {country}" if region else country
            geolocator = Nominatim(user_agent=f"network_tracker_{uuid.uuid4()}")
            location = geolocator.geocode(query)
            
            if location:
                return (location.latitude, location.longitude), None
            location = geolocator.geocode(country)
            if location:
                return (location.latitude, location.longitude), None
            return None, "Location coordinates not found"
        except Exception as e:
            return None, f"Error getting coordinates: {str(e)}"
    
    def create_map(self, phone_info, coordinates):
        """Create an interactive map with the phone number location"""
        try:
            map_location = folium.Map(
                location=coordinates,
                zoom_start=10,
                tiles='OpenStreetMap'
            )
            folium.TileLayer('Cartodb Positron').add_to(map_location)
            folium.TileLayer('Cartodb dark_matter').add_to(map_location)
            
            popup_html = f"""
            <div style="font-family: Arial; padding: 5px;">
                <h4 style="margin-bottom: 5px;">Phone Information</h4>
                <hr style="margin: 2px 0;">
                <b>Number:</b> {phone_info['formatted_number']}<br>
                <b>Region:</b> {phone_info['region'] or 'Unknown'}<br>
                <b>Carrier:</b> {phone_info['carrier'] or 'Unknown'}<br>
                <b>Country Code:</b> +{phone_info['country_code']}<br>
                <b>Timezone:</b> {', '.join(phone_info['timezone'])}<br>
                <small>Tracked on: {phone_info['timestamp']}</small>
            </div>
            """
            
            folium.Marker(
                location=coordinates,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"Phone: {phone_info['formatted_number']}",
                icon=folium.Icon(color="red", icon="phone", prefix="fa")
            ).add_to(map_location)
            
            folium.Circle(
                location=coordinates,
                radius=20000,
                color="blue",
                weight=2,
                fill=True,
                fill_color="blue",
                fill_opacity=0.1,
                tooltip="Approximate Coverage Area"
            ).add_to(map_location)
            
            folium.LayerControl().add_to(map_location)
            Fullscreen().add_to(map_location)
            map_location.add_child(MeasureControl())
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            map_file = f"phone_location_{timestamp}.html"
            map_location.save(map_file)
            
            return map_file, None
        except Exception as e:
            return None, f"Error creating map: {str(e)}"
    
    def track_ip(self, ip_address):
        """Track information about an IP address"""
        try:
            print(f"\n{Colors.BOLD}Tracking IP address: {Colors.BLUE}{ip_address}{Colors.ENDC}\n")
            response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=10)
            data = response.json()
            
            if data.get("status") == "fail":
                return None, f"Error: {data.get('message', 'Unable to track this IP')}"
            
            data['type'] = "ip"
            data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history.append(data)
            if len(self.history) > 50:
                self.history = self.history[-50:]
            self.save_history()
            
            return data, None
        except requests.RequestException as e:
            return None, f"Connection Error: {e}"
        except Exception as e:
            return None, f"An error occurred: {str(e)}"
    
    def scan_ports(self, ip_address, port_range=None):
        """Scan for open ports on the specified IP address"""
        if not port_range:
            port_range = range(1, 1025)
        
        print(f"\n{Colors.BOLD}Scanning ports for: {Colors.BLUE}{ip_address}{Colors.ENDC}")
        print(f"{Colors.CYAN}Scanning ports {port_range.start} to {port_range.stop-1}...{Colors.ENDC}")
        
        open_ports = []
        socket.setdefaulttimeout(0.5)
        
        def scan_port(port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip_address, port))
            if result == 0:
                service = self.get_service_name(port)
                open_ports.append((port, service))
                print(f"{Colors.GREEN}[+] Port {port:5d} is open: {service}{Colors.ENDC}")
            sock.close()
        
        threads = []
        for port in port_range:
            thread = threading.Thread(target=scan_port, args=(port,))
            threads.append(thread)
            thread.start()
            if len(threads) >= 50:
                for t in threads:
                    t.join()
                threads = []
        
        for t in threads:
            t.join()
        
        return open_ports
    
    def get_service_name(self, port):
        """Get common service name for a port"""
        common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
            3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Proxy",
            8443: "HTTPS-Alt"
        }
        return common_ports.get(port, "Unknown Service")
    
    def display_phone_info(self, data):
        """Display phone number information"""
        print(f"\n{Colors.GREEN}╔══════════════ PHONE INFORMATION ══════════════╗{Colors.ENDC}")
        print(f"{Colors.GREEN}║{Colors.ENDC}")
        print(f"{Colors.GREEN}║  {Colors.BOLD}Number:{Colors.ENDC} {data.get('formatted_number', 'N/A')}")
        print(f"{Colors.GREEN}║  {Colors.BOLD}Country Code:{Colors.ENDC} +{data.get('country_code', 'N/A')}")
        print(f"{Colors.GREEN}║  {Colors.BOLD}Region:{Colors.ENDC} {data.get('region', 'N/A')}")
        print(f"{Colors.GREEN}║  {Colors.BOLD}Carrier:{Colors.ENDC} {data.get('carrier', 'N/A')}")
        print(f"{Colors.GREEN}║  {Colors.BOLD}Timezone:{Colors.ENDC} {', '.join(data.get('timezone', ['N/A']))}")
        print(f"{Colors.GREEN}║  {Colors.BOLD}Tracked:{Colors.ENDC} {data.get('timestamp', 'N/A')}")
        print(f"{Colors.GREEN}║{Colors.ENDC}")
        print(f"{Colors.GREEN}╚═══════════════════════════════════════════════╝{Colors.ENDC}")
    
    def display_ip_info(self, data):
        """Display IP address information"""
        print(f"\n{Colors.GREEN}╔══════════════ IP INFORMATION ══════════════╗{Colors.ENDC}")
        print(f"{Colors.GREEN}║{Colors.ENDC}")
        print(f"{Colors.GREEN}║  {Colors.BOLD}IP Address:{Colors.ENDC} {data.get('query', 'N/A')}")
        print(f"{Colors.GREEN}║  {Colors.BOLD}Location:{Colors.ENDC} {data.get('city', 'N/A')}, {data.get('regionName', 'N/A')}, {data.get('country', 'N/A')}")
        print(f"{Colors.GREEN}║  {Colors.BOLD}Zip Code:{Colors.ENDC} {data.get('zip', 'N/A')}")
        print(f"{Colors.GREEN}║  {Colors.BOLD}Coordinates:{Colors.ENDC} {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}")
        print(f"{Colors.GREEN}║  {Colors.BOLD}Timezone:{Colors.ENDC} {data.get('timezone', 'N/A')}")
        print(f"{Colors.GREEN}║  {Colors.BOLD}ISP:{Colors.ENDC} {data.get('isp', 'N/A')}")
        print(f"{Colors.GREEN}║  {Colors.BOLD}Organization:{Colors.ENDC} {data.get('org', 'N/A')}")
        print(f"{Colors.GREEN}║  {Colors.BOLD}Tracked:{Colors.ENDC} {data.get('timestamp', 'N/A')}")
        print(f"{Colors.GREEN}║{Colors.ENDC}")
        print(f"{Colors.GREEN}╚═════════════════════════════════════════════╝{Colors.ENDC}")
    
    def display_history(self):
        """Display search history"""
        if not self.history:
            print(f"\n{Colors.WARNING}No search history found.{Colors.ENDC}")
            return
        
        print(f"\n{Colors.GREEN}╔══════════════ SEARCH HISTORY ══════════════╗{Colors.ENDC}")
        print(f"{Colors.GREEN}║{Colors.ENDC}")
        for i, entry in enumerate(self.history, 1):
            if entry['type'] == 'phone':
                print(f"{Colors.GREEN}║  {Colors.BOLD}[{i}] Phone: {Colors.ENDC} {entry.get('formatted_number', 'N/A')} - {entry.get('timestamp', 'N/A')}")
                print(f"{Colors.GREEN}║      {entry.get('region', 'N/A')}, +{entry.get('country_code', 'N/A')}{Colors.ENDC}")
            else:
                print(f"{Colors.GREEN}║  {Colors.BOLD}[{i}] IP: {Colors.ENDC} {entry.get('query', 'N/A')} - {entry.get('timestamp', 'N/A')}")
                print(f"{Colors.GREEN}║      {entry.get('city', 'N/A')}, {entry.get('country', 'N/A')}{Colors.ENDC}")
            print(f"{Colors.GREEN}║{Colors.ENDC}")
        print(f"{Colors.GREEN}╚═════════════════════════════════════════════╝{Colors.ENDC}")

def show_main_menu():
    """Display the main menu with fade-in animation"""
    menu_lines = [
        "╔══════════════ MAIN MENU ══════════════╗",
        "║                                       ║",
        "║  1. Track Phone Number                ║",
        "║  2. Track IP Address                  ║",
        "║  3. Scan Ports                        ║",
        "║  4. View History                      ║",
        "║  5. About                             ║",
        "║  0. Exit                              ║",
        "║                                       ║",
        "╚═══════════════════════════════════════╝"
    ]
    print(f"\n{Colors.BLUE}", end="")
    fade_in_menu(menu_lines)
    print(f"{Colors.ENDC}", end="")

def show_about():
    """Display information about the tool"""
    clear_screen()
    print_banner()
    print(f"\n{Colors.RED}╔══════════════ ABOUT ══════════════╗{Colors.ENDC}")
    print(f"{Colors.GREEN}║{Colors.ENDC}")
    print(f"{Colors.GREEN}║  {Colors.BOLD}Hell Scanner v1.0{Colors.ENDC}")
    print(f"{Colors.GREEN}║  Created by: Zero{Colors.ENDC}")
    print(f"{Colors.GREEN}║{Colors.ENDC}")
    print(f"{Colors.GREEN}║  Features:{Colors.ENDC}")
    print(f"{Colors.GREEN}║  • Track phone numbers worldwide{Colors.ENDC}")
    print(f"{Colors.GREEN}║  • Track IP addresses with precision{Colors.ENDC}")
    print(f"{Colors.GREEN}║  • Scan for open ports efficiently{Colors.ENDC}")
    print(f"{Colors.GREEN}║  • View search history{Colors.ENDC}")
    print(f"{Colors.GREEN}║{Colors.ENDC}")
    print(f"{Colors.GREEN}║  Dependencies:{Colors.ENDC}")
    print(f"{Colors.GREEN}║  • phonenumbers{Colors.ENDC}")
    print(f"{Colors.GREEN}║  • geopy{Colors.ENDC}")
    print(f"{Colors.GREEN}║  • folium{Colors.ENDC}")
    print(f"{Colors.GREEN}║  • requests{Colors.ENDC}")
    print(f"{Colors.GREEN}║{Colors.ENDC}")
    print(f"{Colors.GREEN}║  Install with:{Colors.ENDC}")
    print(f"{Colors.GREEN}║  pip install phonenumbers geopy folium requests{Colors.ENDC}")
    print(f"{Colors.GREEN}║{Colors.ENDC}")
    print(f"{Colors.GREEN}║  {Colors.WARNING}Use responsibly and only on networks{Colors.ENDC}")
    print(f"{Colors.GREEN}║  {Colors.WARNING}or numbers you have permission to track.{Colors.ENDC}")
    print(f"{Colors.GREEN}║{Colors.ENDC}")
    print(f"{Colors.GREEN}╚═══════════════════════════════════════╝{Colors.ENDC}")

def main():
    """Main application function"""
    tracker = NetworkTracker()
    
    while True:
        clear_screen()
        print_banner()
        show_main_menu()
        
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (0-5): {Colors.ENDC}").strip()
        except EOFError:
            print(f"\n{Colors.CYAN}Input interrupted. Exiting Hell Scanner. Goodbye!{Colors.ENDC}")
            time.sleep(1)
            break
        
        if choice == '0':
            print(f"\n{Colors.CYAN}Thank you for using Hell Scanner. Goodbye!{Colors.ENDC}")
            time.sleep(1)
            break
            
        elif choice == '1':
            clear_screen()
            print_banner()
            print(f"\n{Colors.BOLD}PHONE NUMBER TRACKING{Colors.ENDC}")
            print(f"\n{Colors.WARNING}Enter phone number with country code (e.g., +12025551234){Colors.ENDC}")
            
            while True:
                try:
                    phone_number = input(f"\n{Colors.BOLD}Enter phone number (or 'q' to return): {Colors.ENDC}").strip()
                except EOFError:
                    print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
                    break
                
                if phone_number.lower() == 'q':
                    break
                
                if not phone_number.startswith('+'):
                    print(f"\n{Colors.FAIL}Phone number must start with '+' and country code{Colors.ENDC}")
                    print(f"{Colors.WARNING}Example: +1 for USA, +44 for UK, +91 for India{Colors.ENDC}")
                    continue
                
                progress_bar_animation(f"{Colors.CYAN}Processing phone number...{Colors.ENDC}")
                phone_info, error = tracker.get_phone_info(phone_number)
                
                if error:
                    print(f"\n{Colors.FAIL}{error}{Colors.ENDC}")
                    print(f"{Colors.WARNING}Please try again or enter 'q' to return.{Colors.ENDC}")
                    continue
                
                tracker.display_phone_info(phone_info)
                
                progress_bar_animation(f"{Colors.CYAN}Retrieving geolocation data...{Colors.ENDC}")
                coordinates, coord_error = tracker.get_location_coordinates(phone_number)
                
                if coord_error:
                    print(f"\n{Colors.FAIL}Could not map location: {coord_error}{Colors.ENDC}")
                    try:
                        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
                    except EOFError:
                        print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
                        break
                    break
                
                progress_bar_animation(f"{Colors.CYAN}Generating interactive map...{Colors.ENDC}")
                map_file, map_error = tracker.create_map(phone_info, coordinates)
                
                if map_error:
                    print(f"\n{Colors.FAIL}{map_error}{Colors.ENDC}")
                else:
                    abs_path = os.path.abspath(map_file)
                    print(f"\n{Colors.GREEN}Map created successfully!{Colors.ENDC}")
                    print(f"{Colors.BOLD}Coordinates:{Colors.ENDC} {coordinates[0]:.6f}, {coordinates[1]:.6f}")
                    print(f"{Colors.BOLD}Map file:{Colors.ENDC} {abs_path}")
                    try:
                        print(f"\n{Colors.CYAN}Opening map in default browser...{Colors.ENDC}")
                        time.sleep(1)
                        webbrowser.open('file://' + abs_path)
                    except Exception as e:
                        print(f"\n{Colors.FAIL}Could not open browser: {e}{Colors.ENDC}")
                        print(f"{Colors.WARNING}Please open the HTML file manually.{Colors.ENDC}")
                
                try:
                    another = input(f"\n{Colors.BOLD}Track another number? (y/n): {Colors.ENDC}").strip().lower()
                except EOFError:
                    print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
                    break
                
                if another != 'y':
                    break
                
                clear_screen()
                print_banner()
                print(f"\n{Colors.BOLD}PHONE NUMBER TRACKING{Colors.ENDC}")
                print(f"\n{Colors.WARNING}Enter phone number with country code (e.g., +12025551234){Colors.ENDC}")
        
        elif choice == '2':
            clear_screen()
            print_banner()
            print(f"\n{Colors.BOLD}IP ADDRESS TRACKING{Colors.ENDC}")
            try:
                ip_address = input(f"\n{Colors.BOLD}Enter IP address or domain: {Colors.ENDC}").strip()
            except EOFError:
                print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
                continue
            
            if ip_address:
                try:
                    if not all(c.isdigit() or c == '.' for c in ip_address):
                        progress_bar_animation(f"{Colors.CYAN}Resolving domain name...{Colors.ENDC}")
                        try:
                            ip_addr = socket.gethostbyname(ip_address)
                            print(f"{Colors.GREEN}Domain resolved to: {ip_addr}{Colors.ENDC}")
                        except socket.gaierror:
                            print(f"\n{Colors.FAIL}Unable to resolve domain name.{Colors.ENDC}")
                            try:
                                input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
                            except EOFError:
                                print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
                            continue
                    else:
                        ip_addr = ip_address
                    
                    progress_bar_animation(f"{Colors.CYAN}Tracking IP address...{Colors.ENDC}")
                    ip_data, error = tracker.track_ip(ip_addr)
                    if error:
                        print(f"\n{Colors.FAIL}{error}{Colors.ENDC}")
                    else:
                        tracker.display_ip_info(ip_data)
                except Exception as e:
                    print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}")
            
            try:
                input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
            except EOFError:
                print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
            
        elif choice == '3':
            clear_screen()
            print_banner()
            print(f"\n{Colors.BOLD}PORT SCANNING{Colors.ENDC}")
            print(f"\n{Colors.FAIL}WARNING: Port scanning without permission may be illegal.{Colors.ENDC}")
            print(f"{Colors.WARNING}Only scan IP addresses you own or have permission to scan.{Colors.ENDC}")
            
            try:
                ip_address = input(f"\n{Colors.BOLD}Enter IP address or domain: {Colors.ENDC}").strip()
            except EOFError:
                print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
                continue
            
            if ip_address:
                try:
                    if not all(c.isdigit() or c == '.' for c in ip_address):
                        progress_bar_animation(f"{Colors.CYAN}Resolving domain name...{Colors.ENDC}")
                        try:
                            ip_addr = socket.gethostbyname(ip_address)
                            print(f"{Colors.GREEN}Domain resolved to: {ip_addr}{Colors.ENDC}")
                        except socket.gaierror:
                            print(f"\n{Colors.FAIL}Unable to resolve domain name.{Colors.ENDC}")
                            try:
                                input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
                            except EOFError:
                                print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
                            continue
                    else:
                        ip_addr = ip_address
                    
                    print(f"\n{Colors.BOLD}Select scan type:{Colors.ENDC}")
                    print(f"1. Quick scan (common ports)")
                    print(f"2. Full scan (1-1024)")
                    print(f"3. Custom range")
                    try:
                        scan_type = input(f"\n{Colors.BOLD}Choice (1-3): {Colors.ENDC}").strip()
                    except EOFError:
                        print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
                        continue
                    
                    if scan_type == '1':
                        port_range = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080, 8443]
                        open_ports = []
                        progress_bar_animation(f"{Colors.CYAN}Scanning common ports...{Colors.ENDC}")
                        for port in port_range:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(0.5)
                            result = sock.connect_ex((ip_addr, port))
                            if result == 0:
                                service = tracker.get_service_name(port)
                                open_ports.append((port, service))
                                print(f"{Colors.GREEN}[+] Port {port:5d} is open: {service}{Colors.ENDC}")
                            sock.close()
                    elif scan_type == '2':
                        progress_bar_animation(f"{Colors.CYAN}Scanning ports 1-1024...{Colors.ENDC}")
                        open_ports = tracker.scan_ports(ip_addr, range(1, 1025))
                    elif scan_type == '3':
                        try:
                            start_port = int(input(f"{Colors.BOLD}Enter start port: {Colors.ENDC}"))
                            end_port = int(input(f"{Colors.BOLD}Enter end port: {Colors.ENDC}"))
                            if start_port < 1 or end_port > 65535 or start_port > end_port:
                                print(f"\n{Colors.FAIL}Invalid port range. Ports must be between 1 and 65535.{Colors.ENDC}")
                                try:
                                    input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
                                except EOFError:
                                    print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
                                continue
                            progress_bar_animation(f"{Colors.CYAN}Scanning ports {start_port}-{end_port}...{Colors.ENDC}")
                            open_ports = tracker.scan_ports(ip_addr, range(start_port, end_port + 1))
                        except ValueError:
                            print(f"\n{Colors.FAIL}Invalid input. Please enter numbers only.{Colors.ENDC}")
                            try:
                                input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
                            except EOFError:
                                print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
                            continue
                        except EOFError:
                            print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
                            continue
                    else:
                        print(f"\n{Colors.FAIL}Invalid choice.{Colors.ENDC}")
                        try:
                            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
                        except EOFError:
                            print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
                        continue
                    
                    if open_ports:
                        print(f"\n{Colors.GREEN}╔══════════════ SCAN SUMMARY ══════════════╗{Colors.ENDC}")
                        print(f"{Colors.GREEN}║{Colors.ENDC}")
                        print(f"{Colors.GREEN}║  {Colors.BOLD}Found {len(open_ports)} open port(s) on {ip_addr}{Colors.ENDC}")
                        print(f"{Colors.GREEN}║{Colors.ENDC}")
                        for port, service in open_ports:
                            print(f"{Colors.GREEN}║  {Colors.BOLD}Port {port:5d}:{Colors.ENDC} {service}")
                        print(f"{Colors.GREEN}║{Colors.ENDC}")
                        print(f"{Colors.GREEN}╚═════════════════════════════════════════════╝{Colors.ENDC}")
                    else:
                        print(f"\n{Colors.WARNING}No open ports found.{Colors.ENDC}")
                        
                except Exception as e:
                    print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}")
                    
            try:
                input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
            except EOFError:
                print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
            
        elif choice == '4':
            clear_screen()
            print_banner()
            print(f"\n{Colors.BOLD}SEARCH HISTORY{Colors.ENDC}")
            tracker.display_history()
            try:
                input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
            except EOFError:
                print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
            
        elif choice == '5':
            show_about()
            try:
                input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
            except EOFError:
                print(f"\n{Colors.FAIL}Input interrupted. Returning to main menu.{Colors.ENDC}")
            
        else:
            print(f"\n{Colors.FAIL}Invalid choice. Please enter 0-5.{Colors.ENDC}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.CYAN}Program terminated by user. Goodbye!{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}An unexpected error occurred: {e}{Colors.ENDC}")
        try:
            input(f"\n{Colors.BOLD}Press Enter to exit...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.CYAN}Input interrupted. Exiting Hell Scanner. Goodbye!{Colors.ENDC}")
            sys.exit(1)