# Atom AI Assistant

![App](assets/app.png)

Your intelligent, learning Mac assistant. Atom is an advanced AI assistant that learns from your behavior, manages files, controls apps, analyzes data, and performs complex tasks using voice or text commands. It features persistent memory, broad app integration, and comprehensive system access.

Originally created by [Luke Harries](https://harries.co/) and [Chidi Williams](https://chidiwilliams.com/) at
the [London EA Hackathon, February 2023](https://forum.effectivealtruism.org/events/gTSwA8RoGidjpLnf6/london-ea-hackathon).
Enhanced into Atom AI Assistant with advanced learning and system integration capabilities.

## ✨ **New Atom Capabilities**

🧠 **Learning & Memory**: Remembers your preferences and learns from your usage patterns  
🖥️ **Comprehensive App Access**: Controls Finder, Mail, Calendar, Notes, and all macOS apps  
📊 **Advanced Data Analysis**: Processes CSV, JSON, databases, and complex file analysis  
💾 **Persistent Knowledge**: Stores and retrieves information across sessions  
🔐 **Secure Storage**: Uses macOS Keychain for API key management  
⚡ **Enhanced File Management**: Complete file system operations and analysis  
🖥️ **Terminal Integration**: Direct command execution with output capture  
✨ **Siri-like Interface**: Beautiful glowing placeholder and smooth animations  
🔍 **API Validation**: Comprehensive testing of OpenAI API keys  
📋 **Capability Diagnostics**: Real-time system capability checking and status display

## 🔧 **New Developer Tools**

🧪 **API Testing**: `python test_api_capabilities.py` - Test all API keys and validate connectivity  
🔍 **System Diagnostics**: `python api_validator.py` - Check capabilities and run full diagnostics  
🍎 **Xcode Environment Check**: `python xcode_setup_check.py` - Verify macOS/Xcode setup  
📊 **Capability Monitor**: Built-in GUI panel showing real-time system status

## Requirements

* [FFmpeg](https://ffmpeg.org/)

   ```shell
   # on Ubuntu or Debian
   sudo apt update && sudo apt install ffmpeg

   # on Arch Linux
   sudo pacman -S ffmpeg

   # on MacOS using Homebrew (https://brew.sh/)
   brew install ffmpeg

   # on Windows using Chocolatey (https://chocolatey.org/)
   choco install ffmpeg

   # on Windows using Scoop (https://scoop.sh/)
   scoop install ffmpeg
   ```

## Quick Start

### 🚀 **Easy Setup**
```bash
# 1. Check your system and Xcode environment (macOS only)
python xcode_setup_check.py

# 2. Install dependencies
pip install -r requirements.txt
# or
poetry install

# 3. Set up your OpenAI API key (choose one method)
python keychain_manager.py # Keychain setup (recommended for macOS)
# or use environment: export OPENAI_API_KEY=your_key_here
# or create .env file: echo "OPENAI_API_KEY=your_key_here" > .env

# 4. Test API key and check capabilities
python test_api_capabilities.py
```

### 🎯 **Run Atom**
```bash
# GUI Mode (recommended) - Features Siri-like glowing interface
python gui.py

# CLI Mode  
python main.py "your command here"

# Run system diagnostics
python api_validator.py
```

## How Atom Works

Atom uses multiple AI systems working together:

1. **Voice Processing**: OpenAI's Whisper converts speech to text
2. **Intent Understanding**: Advanced LangChain agents analyze your requests
3. **Learning Engine**: Remembers your patterns and preferences
4. **Multi-Modal Execution**: 
   - AppleScript for macOS app automation
   - JavaScript for browser control
   - Direct file system operations
   - Terminal command execution
   - Data analysis and processing
5. **Memory System**: Persistent storage of learned behaviors and user context
6. **Secure Access**: macOS Keychain integration for credential management

## Example Atom Commands

### 🖥️ **System & Apps**
- "Open my Documents folder and show me the largest files"
- "Create a new calendar event for tomorrow at 2 PM"
- "Send an email to john@example.com with my project update"
- "Take a screenshot and save it to Desktop"

### 📊 **Data Analysis** 
- "Analyze the sales data in expenses.csv and show trends"
- "Compare the file sizes in my Downloads vs Documents"
- "Find all images larger than 5MB on my system"
- "Parse this JSON file and extract the error messages"

### 🧠 **Learning & Memory**
- "Remember that I prefer saving reports to ~/Reports/"
- "What did I work on last Tuesday?"
- "Show me my most frequently used commands"
- "Learn my meeting schedule pattern"

### 🌐 **Web & Research**
- "Research the best restaurants near me and save to Notes"
- "Find the latest news about AI and summarize in 3 points"
- "Compare prices for MacBook Pro on different websites"

### ⚡ **Advanced Operations**
- "Backup my important files to external drive"
- "Clean up old downloads and organize by type"
- "Run system diagnostics and show me disk usage"
- "Find duplicate files in my Pictures folder"
* Play a game of chess. Prompt: "Play a game of chess" -> It will open up Chess.com and start clicking around.

## Learn more

Checkout our blog posts for more information:
- [Chidi's blog post](https://chidiwilliams.com/post/gpt-automator/)
- [Luke's blog post](https://harries.co/ea-hackathon-gpt-automator-and-langchain/)

## Disclaimer

This project executes code generated from natural language and may be susceptible
to [prompt injection](https://en.wikipedia.org/wiki/Prompt_engineering#Prompt_injection) and similar
attacks. This work was made as a proof-of-concept and is not intended for production use.
