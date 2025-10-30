"""
macOS Keychain integration for securely storing and retrieving API keys.
"""
import subprocess
import json
from typing import Optional


class KeychainManager:
    """Manages API keys using macOS Keychain Services."""
    
    SERVICE_NAME = "Atom-AI-Assistant"
    
    @classmethod
    def store_openai_api_key(cls, api_key: str, account_name: str = "openai-api") -> bool:
        """
        Store OpenAI API key in macOS Keychain.
        
        Args:
            api_key: The OpenAI API key to store
            account_name: Account name for the keychain entry
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Delete existing entry if it exists
            cls._delete_keychain_item(account_name)
            
            # Add new entry
            cmd = [
                "security", "add-generic-password",
                "-a", account_name,
                "-s", cls.SERVICE_NAME,
                "-w", api_key,
                "-T", "",  # Allow all applications to access
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            print(f"Error storing API key: {e}")
            return False
    
    @classmethod
    def get_openai_api_key(cls, account_name: str = "openai-api") -> Optional[str]:
        """
        Retrieve OpenAI API key from macOS Keychain.
        
        Args:
            account_name: Account name for the keychain entry
            
        Returns:
            API key if found, None otherwise
        """
        try:
            cmd = [
                "security", "find-generic-password",
                "-a", account_name,
                "-s", cls.SERVICE_NAME,
                "-w"  # Output password only
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return None
                
        except Exception as e:
            print(f"Error retrieving API key: {e}")
            return None
    
    @classmethod
    def _delete_keychain_item(cls, account_name: str) -> bool:
        """Delete existing keychain item if it exists."""
        try:
            cmd = [
                "security", "delete-generic-password",
                "-a", account_name,
                "-s", cls.SERVICE_NAME
            ]
            
            subprocess.run(cmd, capture_output=True, text=True)
            return True  # Don't care about return code, item might not exist
            
        except Exception:
            return False
    
    @classmethod
    def setup_api_key_interactive(cls) -> bool:
        """
        Interactive setup for OpenAI API key.
        Prompts user for API key and stores it in Keychain.
        
        Returns:
            True if successful, False otherwise
        """
        print("\n🔐 Atom AI Assistant - Keychain Setup")
        print("=" * 40)
        print("This will securely store your OpenAI API key in macOS Keychain.")
        print("You can get your API key from: https://platform.openai.com/api-keys")
        print()
        
        try:
            api_key = input("Enter your OpenAI API key: ").strip()
            
            if not api_key:
                print("❌ No API key entered.")
                return False
            
            if not api_key.startswith("sk-"):
                print("⚠️  Warning: OpenAI API keys typically start with 'sk-'")
                confirm = input("Continue anyway? (y/N): ").strip().lower()
                if confirm != 'y':
                    return False
            
            print("\n🔄 Storing API key in Keychain...")
            
            if cls.store_openai_api_key(api_key):
                print("✅ API key successfully stored in Keychain!")
                print("You can now run Atom without a .env file.")
                return True
            else:
                print("❌ Failed to store API key in Keychain.")
                return False
                
        except KeyboardInterrupt:
            print("\n\n❌ Setup cancelled.")
            return False
        except Exception as e:
            print(f"❌ Error during setup: {e}")
            return False


def get_openai_api_key_with_fallback() -> Optional[str]:
    """
    Get OpenAI API key with fallback chain:
    1. Try macOS Keychain
    2. Try environment variable OPENAI_API_KEY
    3. Try .env file
    
    Returns:
        API key if found, None otherwise
    """
    import os
    from dotenv import load_dotenv
    
    # Try Keychain first
    api_key = KeychainManager.get_openai_api_key()
    if api_key:
        print("🔐 Using OpenAI API key from Keychain")
        return api_key
    
    # Try environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("🌍 Using OpenAI API key from environment variable")
        return api_key
    
    # Try .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("📄 Using OpenAI API key from .env file")
        return api_key
    
    print("❌ No OpenAI API key found!")
    print("Options:")
    print("1. Run 'python -c \"from keychain_manager import KeychainManager; KeychainManager.setup_api_key_interactive()\"'")
    print("2. Set OPENAI_API_KEY environment variable")
    print("3. Create a .env file with OPENAI_API_KEY")
    
    return None


if __name__ == "__main__":
    # Interactive setup when run directly
    KeychainManager.setup_api_key_interactive()