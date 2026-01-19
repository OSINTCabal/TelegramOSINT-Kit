# 🔍 TeleGramSint

**Multi-API Intelligence Gathering Platform for Telegram**

A powerful, terminal-based OSINT tool for gathering intelligence from Telegram using multiple free and paid APIs. Features automated free searches, individual paid operations, usage tracking, and beautiful colorized output.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg)

## ✨ Features

### 🆓 Free Search Mode
- **Bot ID Lookup** - Search bot database (BotsArchive)
- **Channel Info** - Basic channel details (Telegram Channel API)
- **Entity Search** - Global search for users/channels (Telegram Scraper)
- Unlimited searches, no API limits

### 💎 Paid Operations (15 free calls/month)
- **Check Participant Status** - Verify if user is in channel/group
- **Fetch Entity by Username** - Get detailed user/channel info
- **Fetch Full User Info** - Complete user profiles
- **Fetch Full Channel Info** - Comprehensive channel data
- **Search User by Phone** - Find users by phone number
- **Fetch Online Users** - Get online members of groups
- **Fetch Stories** - Retrieve user/channel stories
- **Search Entities** - Advanced global search

### 🎨 Additional Features
- **Colorized Output** - Beautiful blue-to-purple gradient for each API
- **Usage Tracking** - Automatic monthly usage counter for paid APIs
- **Secure Config** - API keys stored locally with restrictive permissions
- **Progress Bars** - Visual usage indicators
- **No Dependencies** - Uses only Python standard library + curl

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- curl (usually pre-installed on Linux/macOS)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/TelegramOSINT-Kit.git
cd TelegramOSINT-Kit

# Make executable
chmod +x TelegramOSINT-Kit.py

# Run the tool
./TelegramOSINT-Kit.py
```

### Installing curl (if needed)

**Debian/Ubuntu:**
```bash
sudo apt install curl
```

**macOS:**
```bash
brew install curl
```

**Windows:**
- Download from https://curl.se/windows/
- Or use WSL (Windows Subsystem for Linux)

## 🔑 API Key Setup

The tool requires RapidAPI keys for full functionality.

### Getting API Keys

1. **Sign up for RapidAPI**: https://rapidapi.com/
2. **Subscribe to these APIs** (both have free tiers):
   - [Telegram Channel API](https://rapidapi.com/akrakoro-akrakoro-default/api/telegram-channel) - Free basic plan
   - [Telegram Scraper API](https://rapidapi.com/nyansterowo/api/telegram-scraper-api) - 15 free calls/month

### Configuring Keys

Run the tool and select option **C** (Configure API Keys):

```bash
./TelegramOSINT-Kit.py
# Select: C
# Enter your RapidAPI keys when prompted
```

Keys are stored securely in `~/.tg_osint_config.json` with restrictive permissions (600).

## 🚀 Usage

### Main Menu

```
[MAIN MENU]
  1. Free Search (All Free APIs)    [Unlimited]
  2. Paid Operations Menu            [Requires API keys]

[CONFIGURATION]
  C. Configure API Keys
  V. View Configuration Status

[UTILITIES]
  U. View Usage Stats
  R. Reset Usage Counter
  0. Exit
```

### Free Search Example

```bash
./TelegramOSINT-Kit.py
# Select: 1
# Enter username: osintcabal
```

**Output:** Runs all 3 free APIs automatically:
- Bot ID lookup
- Channel information
- Entity search results

### Paid Operations Example

```bash
./TelegramOSINT-Kit.py
# Select: 2 (Paid Operations Menu)
# Select: 3 (Fetch Full User Info)
# Enter username: target_username
```

**Output:** Complete user profile (uses 1 of 15 monthly calls)

### Batch Processing

For multiple targets, create a simple wrapper:

```bash
#!/bin/bash
for target in $(cat targets.txt); do
    echo "$target" | ./TelegramOSINT-Kit.py
    sleep 2
done
```

## 📊 Usage Tracking

The tool automatically tracks your paid API usage:

- **Monthly limit:** 15 calls (Telegram Scraper API)
- **Auto-reset:** First day of each month
- **Visual indicators:** Progress bars show usage percentage
- **Protection:** Blocks paid calls when limit reached

View current usage: Select **U** from main menu

## 🎨 Color Scheme

Each API has a unique color for easy identification:

**Free APIs:**
- 🔵 Bot ID Lookup - Light Cyan
- 🔷 Channel Info - Medium Blue
- 🟣 Entity Search - Purple

**Paid Operations:**
- 💜 Participant Status - Light Purple
- 🔮 Entity by Username - Blue-Purple
- 🔵 Full User Info - Medium Blue
- 🔷 Full Channel Info - Cyan
- 🌊 User by Phone - Deep Blue
- 💗 Online Users - Magenta
- 🦄 Stories - Violet
- 👑 Search Entities - Royal Purple

## 📁 File Locations

- **Configuration:** `~/.tg_osint_config.json` (API keys)
- **Usage Data:** `~/.tg_osint_usage.json` (monthly tracking)

Both files use restrictive permissions (600) for security.

## 🔒 Security & Privacy

- **Local storage only** - API keys never transmitted except to RapidAPI
- **Restrictive permissions** - Config files are mode 600 (user read/write only)
- **No telemetry** - Tool doesn't phone home or track usage externally
- **OPSEC-friendly** - Compatible with ProxyChains for anonymity

### Using with ProxyChains

```bash
proxychains4 ./TelegramOSINT-Kit.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
git clone https://github.com/yourusername/TelegramOSINT-Kit.git
cd TelegramOSINT-Kit

# No dependencies to install!
# Start developing
```

### Adding New APIs

1. Add function in appropriate section (free/paid)
2. Add menu option
3. Add color scheme
4. Update README

## 📝 Use Cases

- **OSINT Investigations** - Gather intelligence on Telegram entities
- **Threat Intelligence** - Monitor channels for suspicious activity
- **Research** - Academic research on Telegram communities
- **Security Audits** - Verify organization presence on Telegram
- **Due Diligence** - Background checks on Telegram users

## ⚖️ Legal Notice

This tool is for **legitimate OSINT and investigative purposes only**.

Users are responsible for compliance with:
- Telegram Terms of Service
- RapidAPI Terms of Use
- Local privacy and data protection laws
- Applicable professional licensing requirements

**Do not use this tool for:**
- Harassment or stalking
- Unauthorized surveillance
- Violating privacy rights
- Any illegal activities

## 🐛 Troubleshooting

### "curl: command not found"
Install curl: `sudo apt install curl` (Debian/Ubuntu) or `brew install curl` (macOS)

### "API key not configured"
Run option **C** from main menu to configure your RapidAPI keys

### "Monthly limit reached"
Wait until next month or upgrade your RapidAPI subscription

### "No results found"
- Target may not exist
- Target may be private/restricted
- Check username spelling (with or without @)

### Config file permissions error
```bash
chmod 600 ~/.tg_osint_config.json
```

## 📚 API Documentation

- [BotsArchive](https://botsarchive.com/) - Bot database (no key required)
- [Telegram Channel API](https://rapidapi.com/akrakoro-akrakoro-default/api/telegram-channel) - Basic channel info
- [Telegram Scraper API](https://rapidapi.com/nyansterowo/api/telegram-scraper-api) - Advanced features

## 🗺️ Roadmap

- [ ] Export results to CSV/JSON
- [ ] Automated batch processing mode
- [ ] Integration with additional Telegram APIs
- [ ] Web interface for results visualization
- [ ] Historical data archiving
- [ ] Custom report generation

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- BotsArchive for free bot database
- RapidAPI for API infrastructure
- Telegram for their open ecosystem
- OSINT community for inspiration

## 📧 Contact

- **Issues:** [GitHub Issues](https://github.com/yourusername/TelegramOSINT-Kit/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/TelegramOSINT-Kit/discussions)

---

**⭐ If you find this tool useful, please star the repository!**

**Built with ❤️ for the OSINT community**
