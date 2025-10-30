#!/usr/bin/env python3
"""
Setup script for GPT-Automator with enhanced capabilities.
This script helps users set up the OpenAI API key and test the new features.
"""

import sys
import os
from keychain_manager import KeychainManager, get_openai_api_key_with_fallback


def main():
    print("🚀 Atom AI Assistant - Enhanced Setup")
    print("=" * 50)
    print()
    print("This enhanced version includes:")
    print("✅ File management (list, copy, move, delete, analyze files)")
    print("✅ Terminal command execution")
    print("✅ macOS Keychain integration for secure API key storage")
    print("✅ All original browser and AppleScript automation")
    print()
    
    # Check current API key status
    api_key = get_openai_api_key_with_fallback()
    
    if api_key:
        print("✅ OpenAI API key is already configured!")
        print("🔐 Source: Keychain" if KeychainManager.get_openai_api_key() else "📄 Source: Environment/File")
    else:
        print("❌ No OpenAI API key found.")
        setup_choice = input("\nWould you like to set up your API key in Keychain now? (y/N): ").strip().lower()
        
        if setup_choice == 'y':
            if KeychainManager.setup_api_key_interactive():
                print("\n✅ Setup complete!")
            else:
                print("\n❌ Setup failed. Please try again or use environment variables.")
                return False
        else:
            print("\n📝 Alternative setup options:")
            print("1. Set OPENAI_API_KEY environment variable")
            print("2. Create .env file with OPENAI_API_KEY=your_key_here")
            print("3. Run 'python keychain_manager.py' later to use Keychain")
            return False
    
    print("\n🧪 Testing new capabilities...")
    test_new_features()
    
    print("\n🎉 Atom AI Assistant is ready to use!")
    print("\n📚 Example commands you can now use:")
    print('• "List files in my Downloads folder"')
    print('• "Copy important.txt to my Desktop"')
    print('• "What is the size of my Documents folder?"')
    print('• "Run ls -la in my home directory"')
    print('• "Search for files containing \'project\' in my Documents"')
    print('• "Open Chrome and search for restaurants near me"')
    print('• "Calculate 15 * 23 using the calculator"')
    
    print("\n🚀 Start the app:")
    print("• GUI: python gui.py")
    print("• CLI: python main.py 'your command here'")
    
    return True


def test_new_features():
    """Test the new file management and terminal features."""
    from commands import list_directory, run_terminal_command, get_file_info
    
    # Test file management
    try:
        result = list_directory(".")
        print("✅ File management: Working")
    except Exception as e:
        print(f"❌ File management: Error - {e}")
    
    # Test terminal execution
    try:
        result = run_terminal_command("echo 'Hello from terminal!'")
        print("✅ Terminal execution: Working")
    except Exception as e:
        print(f"❌ Terminal execution: Error - {e}")
    
    # Test file info
    try:
        result = get_file_info("README.md")
        print("✅ File analysis: Working")
    except Exception as e:
        print(f"❌ File analysis: Error - {e}")


if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)