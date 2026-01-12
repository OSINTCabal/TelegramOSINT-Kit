#!/usr/bin/env python3
"""
Telegram OSINT Kit
Multi-API intelligence gathering tool for Telegram reconnaissance
GitHub: https://github.com/yourusername/TelegramOSINT-Kit
"""

import subprocess
import sys
import json
import os
from typing import Optional, Dict, Any, List
from datetime import datetime

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    PURPLE = '\033[35m'
    GREY = '\033[90m'
    RED = '\033[91m'

# Configuration
CONFIG_FILE = os.path.expanduser("~/.tg_osint_config.json")
USAGE_FILE = os.path.expanduser("~/.tg_osint_usage.json")

class ConfigManager:
    """Manage API key configuration"""
    
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Load configuration from file"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
            # Set restrictive permissions
            os.chmod(CONFIG_FILE, 0o600)
        except Exception as e:
            print_status(f"Failed to save config: {e}", "error")
    
    def get_api_key(self, key_name: str) -> Optional[str]:
        """Get API key from config"""
        return self.config.get(key_name)
    
    def set_api_key(self, key_name: str, value: str):
        """Set API key in config"""
        self.config[key_name] = value
        self.save_config()
    
    def has_keys(self) -> bool:
        """Check if any keys are configured"""
        return bool(self.config.get('rapidapi_channel_key') or 
                   self.config.get('rapidapi_scraper_key'))

class UsageTracker:
    """Track API usage for paid endpoints"""
    
    def __init__(self):
        self.limits = {
            'telegram_scraper': 15  # Monthly limit
        }
        self.usage = self.load_usage()
    
    def load_usage(self) -> Dict:
        """Load usage data from file"""
        if os.path.exists(USAGE_FILE):
            try:
                with open(USAGE_FILE, 'r') as f:
                    data = json.load(f)
                    # Reset if new month
                    if data.get('month') != datetime.now().strftime('%Y-%m'):
                        return self.reset_usage()
                    return data
            except:
                return self.reset_usage()
        return self.reset_usage()
    
    def reset_usage(self) -> Dict:
        """Reset usage for new month"""
        return {
            'month': datetime.now().strftime('%Y-%m'),
            'telegram_scraper': 0
        }
    
    def save_usage(self):
        """Save usage data to file"""
        try:
            with open(USAGE_FILE, 'w') as f:
                json.dump(self.usage, f, indent=2)
        except Exception as e:
            print_status(f"Failed to save usage data: {e}", "warning")
    
    def can_use(self, api_name: str) -> bool:
        """Check if API can be used"""
        if api_name not in self.limits:
            return True
        return self.usage.get(api_name, 0) < self.limits[api_name]
    
    def increment(self, api_name: str):
        """Increment usage counter"""
        self.usage[api_name] = self.usage.get(api_name, 0) + 1
        self.save_usage()
    
    def get_remaining(self, api_name: str) -> str:
        """Get remaining calls for API"""
        if api_name not in self.limits:
            return "∞"
        used = self.usage.get(api_name, 0)
        limit = self.limits[api_name]
        remaining = limit - used
        return f"{remaining}/{limit}"

def print_banner():
    """Display Telegram ASCII art banner"""
    banner = """
....................................................................................................
....................................................................................................
....................................................................................................
....................................................................................................
....................................................................................................
....................................................................................................
...........................................................................=@@@@@@:.................
......................................................................:@@@@@@@@@@@@@................
..................................................................@@@@@@@@@@@@%*@@@@=...............
.............................................................%@@@@@@@@@@@%......@@@@=...............
........................................................#@@@@@@@@@@@@:.........*@@@@................
...................................................*@@@@@@@@@@@@=..............@@@@@................
..............................................+@@@@@@@@@@@@=..................:@@@@:................
.........................................=@@@@@@@@@@@@+.......................%@@@@.................
....................................=@@@@@@@@@@@@*............#@=.............@@@@#.................
...............................-%@@@@@@@@@@@#.............-@@@@@@%...........=@@@@..................
..........................:%@@@@@@@@@@@#:..............*@@@@@@@@@............@@@@@..................
......................#@@@@@@@@@@@%:...............:@@@@@@@@@@@..............@@@@=..................
.................#@@@@@@@@@@@@-.................*@@@@@@@@@@@@...............#@@@@...................
............*@@@@@@@@@@@@-...................@@@@@@@@@@@@@@.................@@@@%...................
........*@@@@@@@@@@@=....................=@@@@@@@@@@@@@@@..................:@@@@:...................
.......@@@@@@@@+......................@@@@@@@@@%@@@@@@@....................@@@@@....................
.......@@@@@@@....................:@@@@@@@@@-.@@@@@@@......................@@@@*....................
.......:@@@@@@@@@@@:...........#@@@@@@@@@...@@@@@@@.......................+@@@@.....................
..........-@@@@@@@@@@@@@:..:@@@@@@@@@*....@@@@@@@.........................@@@@@.....................
...............-@@@@@@@@@@@@@@@@@@......@@@@@@%..........................:@@@@-.....................
....................-%@@@@@@@@#.......@@@@@@@............................%@@@@......................
.........................@@@@@......@@@@@@%..............................@@@@#......................
..........................@@@@@...=@@@@@%...............................-@@@@.......................
..........................=@@@@#..#@@@@@@@*.............................@@@@@.......................
...........................#@@@@=.#@@@@@@@@@@-..........................@@@@+.......................
............................@@@@@.#@@@@:@@@@@@@@.......................*@@@@........................
.............................@@@@@#@@@@...=@@@@@@@#....................@@@@@........................
..............................@@@@@@@@@.....%@@@@@@@@-................-@@@@:........................
..............................-@@@@@@@@...#@@@@@@@@@@@@@..............%@@@@.........................
...............................*@@@@@@@.*@@@@@@...-@@@@@@@%...........@@@@*.........................
................................@@@@@@@@@@@@@........%@@@@@@@-.......=@@@@..........................
.................................@@@@@@@@@@.............@@@@@@@@.....@@@@@..........................
...................................@@@@@%.................-@@@@@@@%.%@@@@=..........................
.............................................................#@@@@@@@@@@%...........................
................................................................@@@@@@@.............................
....................................................................................................
....................................................................................................
....................................................................................................
"""
    print(f"{Colors.OKCYAN}{banner}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*100}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.PURPLE}                           TELEGRAM OSINT KIT{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.GREY}                  Multi-API Intelligence Gathering Platform{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*100}{Colors.ENDC}\n")

def print_main_menu(tracker: UsageTracker, config: ConfigManager):
    """Display main menu"""
    print(f"\n{Colors.BOLD}{Colors.OKBLUE}[MAIN MENU]{Colors.ENDC}")
    
    if config.has_keys():
        print(f"{Colors.BOLD}Paid API Status:{Colors.ENDC} {tracker.get_remaining('telegram_scraper')} remaining this month")
    else:
        print(f"{Colors.BOLD}{Colors.WARNING}⚠️  API Keys Not Configured{Colors.ENDC}")
    
    print()
    print(f"  {Colors.OKGREEN}1.{Colors.ENDC} Free Search (All Free APIs)    {Colors.GREY}[Unlimited]{Colors.ENDC}")
    print(f"  {Colors.OKGREEN}2.{Colors.ENDC} Paid Operations Menu            {Colors.GREY}[Requires API keys]{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}{Colors.OKBLUE}[CONFIGURATION]{Colors.ENDC}\n")
    print(f"  {Colors.OKGREEN}C.{Colors.ENDC} Configure API Keys")
    print(f"  {Colors.OKGREEN}V.{Colors.ENDC} View Configuration Status")
    
    print(f"\n{Colors.BOLD}{Colors.OKBLUE}[UTILITIES]{Colors.ENDC}\n")
    print(f"  {Colors.OKGREEN}U.{Colors.ENDC} View Usage Stats")
    print(f"  {Colors.OKGREEN}R.{Colors.ENDC} Reset Usage Counter")
    print(f"  {Colors.OKGREEN}0.{Colors.ENDC} Exit\n")

def print_paid_menu(tracker: UsageTracker):
    """Display paid operations menu"""
    print(f"\n{Colors.BOLD}{Colors.PURPLE}[PAID OPERATIONS MENU]{Colors.ENDC}")
    print(f"{Colors.BOLD}Remaining calls:{Colors.ENDC} {tracker.get_remaining('telegram_scraper')}\n")
    
    print(f"  {Colors.PURPLE}1.{Colors.ENDC} Check Participant Status     {Colors.GREY}(Check if user is in channel/group){Colors.ENDC}")
    print(f"  {Colors.PURPLE}2.{Colors.ENDC} Fetch Entity by Username     {Colors.GREY}(Get user/channel by @username){Colors.ENDC}")
    print(f"  {Colors.PURPLE}3.{Colors.ENDC} Fetch Full User Info         {Colors.GREY}(Complete user profile){Colors.ENDC}")
    print(f"  {Colors.PURPLE}4.{Colors.ENDC} Fetch Full Channel Info      {Colors.GREY}(Complete channel details){Colors.ENDC}")
    print(f"  {Colors.PURPLE}5.{Colors.ENDC} Search User by Phone         {Colors.GREY}(Find user by phone number){Colors.ENDC}")
    print(f"  {Colors.PURPLE}6.{Colors.ENDC} Fetch Online Users           {Colors.GREY}(Get online members of group){Colors.ENDC}")
    print(f"  {Colors.PURPLE}7.{Colors.ENDC} Fetch Stories                {Colors.GREY}(Get user/channel stories){Colors.ENDC}")
    print(f"  {Colors.PURPLE}8.{Colors.ENDC} Search Entities              {Colors.GREY}(Global search for channels/users){Colors.ENDC}")
    print(f"\n  {Colors.OKGREEN}0.{Colors.ENDC} Back to Main Menu\n")

def print_status(message: str, status: str = "info"):
    """Print formatted status messages"""
    if status == "success":
        print(f"{Colors.OKGREEN}[+]{Colors.ENDC} {message}")
    elif status == "error":
        print(f"{Colors.FAIL}[!]{Colors.ENDC} {message}")
    elif status == "warning":
        print(f"{Colors.WARNING}[*]{Colors.ENDC} {message}")
    elif status == "paid":
        print(f"{Colors.PURPLE}[$]{Colors.ENDC} {message}")
    elif status == "free":
        print(f"{Colors.OKGREEN}[FREE]{Colors.ENDC} {message}")
    else:
        print(f"{Colors.OKCYAN}[i]{Colors.ENDC} {message}")

def print_json(data: Dict[Any, Any], indent: int = 2):
    """Pretty print JSON data with colors"""
    json_str = json.dumps(data, indent=indent, ensure_ascii=False)
    print(f"{Colors.GREY}{json_str}{Colors.ENDC}")

def print_json_colored(data: Dict[Any, Any], color: str, indent: int = 2):
    """Pretty print JSON data with specific color"""
    json_str = json.dumps(data, indent=indent, ensure_ascii=False)
    print(f"{color}{json_str}{Colors.ENDC}")

def curl_request(url: str, headers: Optional[Dict[str, str]] = None) -> Optional[Dict[Any, Any]]:
    """Execute curl command and return JSON response"""
    cmd = ["curl", "-s", "-X", "GET"]
    
    if headers:
        for key, value in headers.items():
            cmd.extend(["-H", f"{key}: {value}"])
    
    cmd.append(url)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0 and result.stdout:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"raw_response": result.stdout}
        else:
            print_status(f"Curl error: {result.stderr}", "error")
            return None
    except subprocess.TimeoutExpired:
        print_status("Request timed out", "error")
        return None
    except Exception as e:
        print_status(f"Error: {str(e)}", "error")
        return None

# ============================================================================
# FREE API FUNCTIONS
# ============================================================================

def get_bot_id(username: str) -> Optional[Dict[Any, Any]]:
    """Get bot ID from BotsArchive [FREE]"""
    if not username.startswith('@'):
        username = f'@{username}'
    
    print_status(f"Bot ID Lookup: {Colors.BOLD}{username}{Colors.ENDC}", "free")
    url = f"https://botsarchive.com/getBotID.php?username={username}"
    
    return curl_request(url)

def get_channel_info_free(channel: str, rapidapi_key: str) -> Optional[Dict[Any, Any]]:
    """Get Telegram channel info from Telegram Channel API [FREE]"""
    channel = channel.lstrip('@')
    
    print_status(f"Channel Info: {Colors.BOLD}@{channel}{Colors.ENDC}", "free")
    url = f"https://telegram-channel.p.rapidapi.com/channel/info?channel={channel}"
    
    headers = {
        'x-rapidapi-host': 'telegram-channel.p.rapidapi.com',
        'x-rapidapi-key': rapidapi_key
    }
    
    return curl_request(url, headers)

def entity_search_free(query: str, rapidapi_key: str, limit: int = 10) -> Optional[Dict[Any, Any]]:
    """Search for entities using Telegram Scraper [FREE]"""
    print_status(f"Entity Search: {Colors.BOLD}{query}{Colors.ENDC}", "free")
    url = f"https://telegram-scraper-api.p.rapidapi.com/entity/search?q={query}&limit={limit}"
    
    headers = {
        'x-rapidapi-host': 'telegram-scraper-api.p.rapidapi.com',
        'x-rapidapi-key': rapidapi_key
    }
    
    return curl_request(url, headers)

# ============================================================================
# PAID API FUNCTIONS (Telegram Scraper)
# ============================================================================

def check_participant_status(peer: str, participant: str, rapidapi_key: str, tracker: UsageTracker) -> Optional[Dict[Any, Any]]:
    """Check if participant is in a chat [PAID]"""
    if not tracker.can_use('telegram_scraper'):
        print_status(f"Monthly limit reached ({tracker.limits['telegram_scraper']} calls).", "error")
        return None
    
    peer = peer.lstrip('@')
    participant = participant.lstrip('@')
    print_status(f"Checking if @{participant} is in @{peer}", "paid")
    url = f"https://telegram-scraper-api.p.rapidapi.com/entity/get-participant?peer={peer}&participant={participant}"
    
    headers = {
        'x-rapidapi-host': 'telegram-scraper-api.p.rapidapi.com',
        'x-rapidapi-key': rapidapi_key
    }
    
    result = curl_request(url, headers)
    if result:
        tracker.increment('telegram_scraper')
        print_status(f"API call recorded. Remaining: {tracker.get_remaining('telegram_scraper')}", "paid")
    return result

def fetch_entity_by_username(peer: str, rapidapi_key: str, tracker: UsageTracker) -> Optional[Dict[Any, Any]]:
    """Fetch entity by username [PAID]"""
    if not tracker.can_use('telegram_scraper'):
        print_status(f"Monthly limit reached ({tracker.limits['telegram_scraper']} calls).", "error")
        return None
    
    peer = peer.lstrip('@')
    print_status(f"Fetching entity: @{peer}", "paid")
    url = f"https://telegram-scraper-api.p.rapidapi.com/entity/fetch?peer={peer}"
    
    headers = {
        'x-rapidapi-host': 'telegram-scraper-api.p.rapidapi.com',
        'x-rapidapi-key': rapidapi_key
    }
    
    result = curl_request(url, headers)
    if result:
        tracker.increment('telegram_scraper')
        print_status(f"API call recorded. Remaining: {tracker.get_remaining('telegram_scraper')}", "paid")
    return result

def fetch_full_user_info(peer: str, rapidapi_key: str, tracker: UsageTracker) -> Optional[Dict[Any, Any]]:
    """Fetch full user info [PAID]"""
    if not tracker.can_use('telegram_scraper'):
        print_status(f"Monthly limit reached ({tracker.limits['telegram_scraper']} calls).", "error")
        return None
    
    peer = peer.lstrip('@')
    print_status(f"Fetching full user info: @{peer}", "paid")
    url = f"https://telegram-scraper-api.p.rapidapi.com/user/full?peer={peer}"
    
    headers = {
        'x-rapidapi-host': 'telegram-scraper-api.p.rapidapi.com',
        'x-rapidapi-key': rapidapi_key
    }
    
    result = curl_request(url, headers)
    if result:
        tracker.increment('telegram_scraper')
        print_status(f"API call recorded. Remaining: {tracker.get_remaining('telegram_scraper')}", "paid")
    return result

def fetch_full_channel_info(peer: str, rapidapi_key: str, tracker: UsageTracker) -> Optional[Dict[Any, Any]]:
    """Fetch full channel info [PAID]"""
    if not tracker.can_use('telegram_scraper'):
        print_status(f"Monthly limit reached ({tracker.limits['telegram_scraper']} calls).", "error")
        return None
    
    peer = peer.lstrip('@')
    print_status(f"Fetching full channel info: @{peer}", "paid")
    url = f"https://telegram-scraper-api.p.rapidapi.com/entity/fullchannel?peer={peer}"
    
    headers = {
        'x-rapidapi-host': 'telegram-scraper-api.p.rapidapi.com',
        'x-rapidapi-key': rapidapi_key
    }
    
    result = curl_request(url, headers)
    if result:
        tracker.increment('telegram_scraper')
        print_status(f"API call recorded. Remaining: {tracker.get_remaining('telegram_scraper')}", "paid")
    return result

def search_user_by_phone(phone: str, rapidapi_key: str, tracker: UsageTracker) -> Optional[Dict[Any, Any]]:
    """Search user by phone number [PAID]"""
    if not tracker.can_use('telegram_scraper'):
        print_status(f"Monthly limit reached ({tracker.limits['telegram_scraper']} calls).", "error")
        return None
    
    print_status(f"Searching by phone: {phone}", "paid")
    url = f"https://telegram-scraper-api.p.rapidapi.com/user/search-by-phone?phone={phone}"
    
    headers = {
        'x-rapidapi-host': 'telegram-scraper-api.p.rapidapi.com',
        'x-rapidapi-key': rapidapi_key
    }
    
    result = curl_request(url, headers)
    if result:
        tracker.increment('telegram_scraper')
        print_status(f"API call recorded. Remaining: {tracker.get_remaining('telegram_scraper')}", "paid")
    return result

def fetch_online_users(peer: str, rapidapi_key: str, tracker: UsageTracker) -> Optional[Dict[Any, Any]]:
    """Fetch online users in a group [PAID]"""
    if not tracker.can_use('telegram_scraper'):
        print_status(f"Monthly limit reached ({tracker.limits['telegram_scraper']} calls).", "error")
        return None
    
    peer = peer.lstrip('@')
    print_status(f"Fetching online users: @{peer}", "paid")
    url = f"https://telegram-scraper-api.p.rapidapi.com/entity/online?peer={peer}"
    
    headers = {
        'x-rapidapi-host': 'telegram-scraper-api.p.rapidapi.com',
        'x-rapidapi-key': rapidapi_key
    }
    
    result = curl_request(url, headers)
    if result:
        tracker.increment('telegram_scraper')
        print_status(f"API call recorded. Remaining: {tracker.get_remaining('telegram_scraper')}", "paid")
    return result

def fetch_stories(peer: str, rapidapi_key: str, tracker: UsageTracker, without_media: bool = False) -> Optional[Dict[Any, Any]]:
    """Fetch stories [PAID]"""
    if not tracker.can_use('telegram_scraper'):
        print_status(f"Monthly limit reached ({tracker.limits['telegram_scraper']} calls).", "error")
        return None
    
    peer = peer.lstrip('@')
    print_status(f"Fetching stories: @{peer}", "paid")
    url = f"https://telegram-scraper-api.p.rapidapi.com/stories/fetch?peer={peer}&withoutMedia={'true' if without_media else 'false'}"
    
    headers = {
        'x-rapidapi-host': 'telegram-scraper-api.p.rapidapi.com',
        'x-rapidapi-key': rapidapi_key
    }
    
    result = curl_request(url, headers)
    if result:
        tracker.increment('telegram_scraper')
        print_status(f"API call recorded. Remaining: {tracker.get_remaining('telegram_scraper')}", "paid")
    return result

def search_entities_paid(query: str, rapidapi_key: str, tracker: UsageTracker, limit: int = 10) -> Optional[Dict[Any, Any]]:
    """Search entities globally [PAID]"""
    if not tracker.can_use('telegram_scraper'):
        print_status(f"Monthly limit reached ({tracker.limits['telegram_scraper']} calls).", "error")
        return None
    
    print_status(f"Searching entities: {query}", "paid")
    url = f"https://telegram-scraper-api.p.rapidapi.com/entity/search?q={query}&limit={limit}"
    
    headers = {
        'x-rapidapi-host': 'telegram-scraper-api.p.rapidapi.com',
        'x-rapidapi-key': rapidapi_key
    }
    
    result = curl_request(url, headers)
    if result:
        tracker.increment('telegram_scraper')
        print_status(f"API call recorded. Remaining: {tracker.get_remaining('telegram_scraper')}", "paid")
    return result

# ============================================================================
# SEARCH MODES
# ============================================================================

def free_search_all(target: str, rapidapi_channel_key: str, rapidapi_scraper_key: str):
    """Run all free APIs on target"""
    print(f"\n{Colors.BOLD}{Colors.PURPLE}[FREE SEARCH - ALL FREE APIS]{Colors.ENDC}\n")
    print(f"{Colors.BOLD}Target:{Colors.ENDC} {Colors.OKCYAN}{target}{Colors.ENDC}\n")
    print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}\n")
    
    results = {}
    
    # 1. Bot ID Lookup - Light Blue
    print(f"{Colors.BOLD}{Colors.OKCYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKCYAN}║{Colors.ENDC} {Colors.BOLD}1. Bot ID Lookup (BotsArchive){Colors.ENDC}                                           {Colors.BOLD}{Colors.OKCYAN}║{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKCYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
    bot_result = get_bot_id(target)
    if bot_result:
        results['bot_id'] = bot_result
        print_json_colored(bot_result, Colors.OKCYAN)
    else:
        print_status("No bot data found", "warning")
    print()
    
    # 2. Channel Info - Medium Blue
    if rapidapi_channel_key:
        print(f"{Colors.BOLD}{Colors.OKBLUE}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.OKBLUE}║{Colors.ENDC} {Colors.BOLD}2. Channel Info (Telegram Channel API){Colors.ENDC}                                    {Colors.BOLD}{Colors.OKBLUE}║{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.OKBLUE}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        channel_result = get_channel_info_free(target, rapidapi_channel_key)
        if channel_result:
            results['channel_info'] = channel_result
            print_json_colored(channel_result, Colors.OKBLUE)
        else:
            print_status("No channel data found", "warning")
        print()
    else:
        print_status("Telegram Channel API key not configured - skipping", "warning")
        print()
    
    # 3. Entity Search - Purple
    if rapidapi_scraper_key:
        print(f"{Colors.BOLD}{Colors.PURPLE}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.PURPLE}║{Colors.ENDC} {Colors.BOLD}3. Entity Search (Telegram Scraper - Free tier){Colors.ENDC}                           {Colors.BOLD}{Colors.PURPLE}║{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.PURPLE}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        search_result = entity_search_free(target, rapidapi_scraper_key)
        if search_result:
            results['entity_search'] = search_result
            print_json_colored(search_result, Colors.PURPLE)
        else:
            print_status("No search results", "warning")
    else:
        print_status("Telegram Scraper API key not configured - skipping", "warning")
    
    return results

def paid_operations_menu(rapidapi_scraper_key: str, tracker: UsageTracker):
    """Interactive paid operations menu"""
    
    if not rapidapi_scraper_key:
        print_status("Telegram Scraper API key not configured. Use option 'C' to configure.", "error")
        input(f"\n{Colors.GREY}Press Enter to continue...{Colors.ENDC}")
        return
    
    while True:
        print_paid_menu(tracker)
        
        choice = input(f"{Colors.BOLD}{Colors.PURPLE}Select paid operation:{Colors.ENDC} ").strip()
        
        if choice == "0":
            break
        
        elif choice == "1":
            # Check Participant Status - Light Purple
            print(f"\n{Colors.BOLD}{Colors.PURPLE}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.PURPLE}║{Colors.ENDC} {Colors.BOLD}CHECK PARTICIPANT STATUS{Colors.ENDC}                                                  {Colors.BOLD}{Colors.PURPLE}║{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.PURPLE}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
            peer = input(f"Enter channel/group username: ").strip()
            participant = input(f"Enter participant username: ").strip()
            if peer and participant:
                result = check_participant_status(peer, participant, rapidapi_scraper_key, tracker)
                if result:
                    print_json_colored(result, '\033[38;5;141m')
        
        elif choice == "2":
            # Fetch Entity by Username - Blue-Purple
            print(f"\n{Colors.BOLD}\033[38;5;105m╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}\033[38;5;105m║{Colors.ENDC} {Colors.BOLD}FETCH ENTITY BY USERNAME{Colors.ENDC}                                                  {Colors.BOLD}\033[38;5;105m║{Colors.ENDC}")
            print(f"{Colors.BOLD}\033[38;5;105m╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
            peer = input(f"Enter username: ").strip()
            if peer:
                result = fetch_entity_by_username(peer, rapidapi_scraper_key, tracker)
                if result:
                    print_json_colored(result, '\033[38;5;105m')
        
        elif choice == "3":
            # Fetch Full User Info - Medium Blue
            print(f"\n{Colors.BOLD}{Colors.OKBLUE}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.OKBLUE}║{Colors.ENDC} {Colors.BOLD}FETCH FULL USER INFO{Colors.ENDC}                                                      {Colors.BOLD}{Colors.OKBLUE}║{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.OKBLUE}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
            peer = input(f"Enter username: ").strip()
            if peer:
                result = fetch_full_user_info(peer, rapidapi_scraper_key, tracker)
                if result:
                    print_json_colored(result, Colors.OKBLUE)
        
        elif choice == "4":
            # Fetch Full Channel Info - Cyan
            print(f"\n{Colors.BOLD}{Colors.OKCYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.OKCYAN}║{Colors.ENDC} {Colors.BOLD}FETCH FULL CHANNEL INFO{Colors.ENDC}                                                   {Colors.BOLD}{Colors.OKCYAN}║{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.OKCYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
            peer = input(f"Enter channel username: ").strip()
            if peer:
                result = fetch_full_channel_info(peer, rapidapi_scraper_key, tracker)
                if result:
                    print_json_colored(result, Colors.OKCYAN)
        
        elif choice == "5":
            # Search User by Phone - Deep Blue
            print(f"\n{Colors.BOLD}\033[38;5;27m╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}\033[38;5;27m║{Colors.ENDC} {Colors.BOLD}SEARCH USER BY PHONE{Colors.ENDC}                                                      {Colors.BOLD}\033[38;5;27m║{Colors.ENDC}")
            print(f"{Colors.BOLD}\033[38;5;27m╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
            phone = input(f"Enter phone number (with country code): ").strip()
            if phone:
                result = search_user_by_phone(phone, rapidapi_scraper_key, tracker)
                if result:
                    print_json_colored(result, '\033[38;5;27m')
        
        elif choice == "6":
            # Fetch Online Users - Magenta
            print(f"\n{Colors.BOLD}\033[38;5;170m╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}\033[38;5;170m║{Colors.ENDC} {Colors.BOLD}FETCH ONLINE USERS{Colors.ENDC}                                                        {Colors.BOLD}\033[38;5;170m║{Colors.ENDC}")
            print(f"{Colors.BOLD}\033[38;5;170m╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
            peer = input(f"Enter group username: ").strip()
            if peer:
                result = fetch_online_users(peer, rapidapi_scraper_key, tracker)
                if result:
                    print_json_colored(result, '\033[38;5;170m')
        
        elif choice == "7":
            # Fetch Stories - Violet
            print(f"\n{Colors.BOLD}\033[38;5;135m╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}\033[38;5;135m║{Colors.ENDC} {Colors.BOLD}FETCH STORIES{Colors.ENDC}                                                             {Colors.BOLD}\033[38;5;135m║{Colors.ENDC}")
            print(f"{Colors.BOLD}\033[38;5;135m╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
            peer = input(f"Enter username: ").strip()
            if peer:
                result = fetch_stories(peer, rapidapi_scraper_key, tracker)
                if result:
                    print_json_colored(result, '\033[38;5;135m')
        
        elif choice == "8":
            # Search Entities - Royal Purple
            print(f"\n{Colors.BOLD}\033[38;5;93m╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}\033[38;5;93m║{Colors.ENDC} {Colors.BOLD}SEARCH ENTITIES{Colors.ENDC}                                                           {Colors.BOLD}\033[38;5;93m║{Colors.ENDC}")
            print(f"{Colors.BOLD}\033[38;5;93m╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
            query = input(f"Enter search query: ").strip()
            limit = input(f"Number of results [default: 10]: ").strip()
            limit = int(limit) if limit else 10
            if query:
                result = search_entities_paid(query, rapidapi_scraper_key, tracker, limit)
                if result:
                    print_json_colored(result, '\033[38;5;93m')
        
        else:
            print_status("Invalid option", "error")
        
        input(f"\n{Colors.GREY}Press Enter to continue...{Colors.ENDC}")
        print("\n" * 2)

def configure_api_keys(config: ConfigManager):
    """Interactive API key configuration"""
    print(f"\n{Colors.BOLD}{Colors.PURPLE}[API KEY CONFIGURATION]{Colors.ENDC}\n")
    print(f"Configure your RapidAPI keys for Telegram intelligence gathering.\n")
    print(f"{Colors.BOLD}Available APIs:{Colors.ENDC}")
    print(f"  1. Telegram Channel API (Free tier - basic channel info)")
    print(f"  2. Telegram Scraper API (15 free calls/month - advanced features)\n")
    
    print(f"{Colors.OKGREEN}Get your keys at:{Colors.ENDC}")
    print(f"  • https://rapidapi.com/akrakoro-akrakoro-default/api/telegram-channel")
    print(f"  • https://rapidapi.com/nyansterowo/api/telegram-scraper-api\n")
    
    # Telegram Channel API
    current_channel = config.get_api_key('rapidapi_channel_key')
    if current_channel:
        print(f"Current Telegram Channel API key: {current_channel[:20]}...")
        update = input(f"Update? (y/n): ").strip().lower()
        if update == 'y':
            key = input(f"Enter new Telegram Channel API key: ").strip()
            if key:
                config.set_api_key('rapidapi_channel_key', key)
                print_status("Telegram Channel API key updated", "success")
    else:
        key = input(f"Enter Telegram Channel API key (or press Enter to skip): ").strip()
        if key:
            config.set_api_key('rapidapi_channel_key', key)
            print_status("Telegram Channel API key saved", "success")
    
    print()
    
    # Telegram Scraper API
    current_scraper = config.get_api_key('rapidapi_scraper_key')
    if current_scraper:
        print(f"Current Telegram Scraper API key: {current_scraper[:20]}...")
        update = input(f"Update? (y/n): ").strip().lower()
        if update == 'y':
            key = input(f"Enter new Telegram Scraper API key: ").strip()
            if key:
                config.set_api_key('rapidapi_scraper_key', key)
                print_status("Telegram Scraper API key updated", "success")
    else:
        key = input(f"Enter Telegram Scraper API key (or press Enter to skip): ").strip()
        if key:
            config.set_api_key('rapidapi_scraper_key', key)
            print_status("Telegram Scraper API key saved", "success")
    
    print()
    print_status(f"Configuration saved to {CONFIG_FILE}", "success")

def view_config_status(config: ConfigManager):
    """Display configuration status"""
    print(f"\n{Colors.BOLD}{Colors.PURPLE}[CONFIGURATION STATUS]{Colors.ENDC}\n")
    
    channel_key = config.get_api_key('rapidapi_channel_key')
    scraper_key = config.get_api_key('rapidapi_scraper_key')
    
    if channel_key:
        print(f"{Colors.OKGREEN}✓{Colors.ENDC} Telegram Channel API: Configured ({channel_key[:20]}...)")
    else:
        print(f"{Colors.FAIL}✗{Colors.ENDC} Telegram Channel API: Not configured")
    
    if scraper_key:
        print(f"{Colors.OKGREEN}✓{Colors.ENDC} Telegram Scraper API: Configured ({scraper_key[:20]}...)")
    else:
        print(f"{Colors.FAIL}✗{Colors.ENDC} Telegram Scraper API: Not configured")
    
    print(f"\n{Colors.GREY}Config file: {CONFIG_FILE}{Colors.ENDC}")

def view_usage_stats(tracker: UsageTracker):
    """Display usage statistics"""
    print(f"\n{Colors.BOLD}{Colors.PURPLE}[USAGE STATISTICS]{Colors.ENDC}\n")
    print(f"{Colors.BOLD}Month:{Colors.ENDC} {tracker.usage.get('month', 'N/A')}\n")
    
    print(f"{Colors.BOLD}Telegram Scraper API (PAID):{Colors.ENDC}")
    used = tracker.usage.get('telegram_scraper', 0)
    limit = tracker.limits['telegram_scraper']
    remaining = limit - used
    percentage = (used / limit) * 100
    
    # Progress bar
    bar_length = 40
    filled = int(bar_length * used / limit)
    bar = '█' * filled + '░' * (bar_length - filled)
    
    color = Colors.OKGREEN if remaining > 5 else Colors.WARNING if remaining > 2 else Colors.FAIL
    
    print(f"  Used: {color}{used}{Colors.ENDC}/{limit}")
    print(f"  Remaining: {color}{remaining}{Colors.ENDC}")
    print(f"  {bar} {color}{percentage:.1f}%{Colors.ENDC}\n")
    
    if remaining == 0:
        next_month = datetime.now().replace(day=1, month=datetime.now().month % 12 + 1)
        print(f"{Colors.FAIL}⚠️  LIMIT REACHED - Resets on {next_month.strftime('%Y-%m-01')}{Colors.ENDC}\n")

def main():
    """Main application loop"""
    config = ConfigManager()
    tracker = UsageTracker()
    print_banner()
    
    # Check if keys are configured
    if not config.has_keys():
        print(f"{Colors.WARNING}⚠️  No API keys configured. Some features will be limited.{Colors.ENDC}")
        print(f"Use option 'C' to configure your RapidAPI keys.\n")
        input(f"{Colors.GREY}Press Enter to continue...{Colors.ENDC}")
    
    while True:
        print_main_menu(tracker, config)
        
        try:
            choice = input(f"{Colors.BOLD}{Colors.OKCYAN}Select option:{Colors.ENDC} ").strip().upper()
            
            if choice == "0":
                print(f"\n{Colors.OKGREEN}Exiting... Stay safe out there! 🔍{Colors.ENDC}\n")
                sys.exit(0)
            
            elif choice == "1":
                # Free Search (All Free APIs)
                target = input(f"{Colors.OKCYAN}Enter username/ID to search:{Colors.ENDC} ").strip()
                if target:
                    channel_key = config.get_api_key('rapidapi_channel_key')
                    scraper_key = config.get_api_key('rapidapi_scraper_key')
                    free_search_all(target, channel_key, scraper_key)
            
            elif choice == "2":
                # Paid Operations Menu
                scraper_key = config.get_api_key('rapidapi_scraper_key')
                paid_operations_menu(scraper_key, tracker)
            
            elif choice == "C":
                # Configure API Keys
                configure_api_keys(config)
            
            elif choice == "V":
                # View Configuration Status
                view_config_status(config)
            
            elif choice == "U":
                # View Usage Stats
                view_usage_stats(tracker)
            
            elif choice == "R":
                # Reset Usage Counter
                print(f"\n{Colors.WARNING}Are you sure you want to reset the usage counter?{Colors.ENDC}")
                confirm = input(f"{Colors.OKCYAN}Type 'YES' to confirm:{Colors.ENDC} ").strip()
                if confirm == "YES":
                    tracker.usage = tracker.reset_usage()
                    tracker.save_usage()
                    print_status("Usage counter reset successfully", "success")
                else:
                    print_status("Reset cancelled", "info")
            
            else:
                print_status("Invalid option", "error")
            
            # Pause before returning to menu
            input(f"\n{Colors.GREY}Press Enter to continue...{Colors.ENDC}")
            print("\n" * 2)
        
        except KeyboardInterrupt:
            print(f"\n\n{Colors.WARNING}[*] Interrupted by user{Colors.ENDC}")
            print(f"{Colors.OKGREEN}Exiting... Stay safe out there! 🔍{Colors.ENDC}\n")
            sys.exit(0)
        except Exception as e:
            print_status(f"Unexpected error: {str(e)}", "error")
            import traceback
            traceback.print_exc()
            input(f"\n{Colors.GREY}Press Enter to continue...{Colors.ENDC}")

if __name__ == "__main__":
    main()
