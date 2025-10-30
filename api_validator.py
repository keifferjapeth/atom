"""
API Key Validator and Capability Checker for Atom AI Assistant.
Tests OpenAI API connectivity and validates system capabilities.
"""
import os
import sys
from typing import Dict, Optional, Tuple
from keychain_manager import get_openai_api_key_with_fallback


def validate_openai_api_key(api_key: Optional[str] = None) -> Tuple[bool, str]:
    """
    Validate OpenAI API key by making a test API call.
    
    Args:
        api_key: Optional API key to test. If None, will use fallback chain.
        
    Returns:
        Tuple of (is_valid, message)
    """
    if api_key is None:
        api_key = get_openai_api_key_with_fallback()
    
    if not api_key:
        return False, "No API key found"
    
    if not api_key.startswith("sk-"):
        return False, "API key format invalid (should start with 'sk-')"
    
    try:
        import openai
        openai.api_key = api_key
        
        # Make a minimal test API call to verify the key works
        # Using the models endpoint as it's lightweight
        models = openai.Model.list()
        
        if models and len(models.get('data', [])) > 0:
            return True, "API key is valid and working"
        else:
            return False, "API key accepted but no models available"
            
    except openai.error.AuthenticationError:
        return False, "API key authentication failed"
    except openai.error.RateLimitError:
        return False, "API rate limit exceeded (but key is valid)"
    except openai.error.APIError as e:
        return False, f"OpenAI API error: {str(e)}"
    except ImportError:
        return False, "OpenAI package not installed"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def check_atom_capabilities() -> Dict[str, Dict[str, any]]:
    """
    Check which Atom capabilities are available on the system.
    
    Returns:
        Dictionary with capability status for each feature area
    """
    capabilities = {
        "core": {
            "status": "unknown",
            "features": []
        },
        "app_integrations": {
            "status": "unknown",
            "features": []
        },
        "learning_system": {
            "status": "unknown",
            "features": []
        },
        "data_analysis": {
            "status": "unknown",
            "features": []
        },
        "voice_recognition": {
            "status": "unknown",
            "features": []
        },
        "macos_integration": {
            "status": "unknown",
            "features": []
        }
    }
    
    # Check core capabilities
    try:
        import langchain
        from commands import computer_applescript_action, chrome_open_url
        capabilities["core"]["status"] = "available"
        capabilities["core"]["features"] = [
            "LangChain integration",
            "AppleScript automation",
            "Chrome browser control"
        ]
    except ImportError as e:
        capabilities["core"]["status"] = "unavailable"
        capabilities["core"]["error"] = str(e)
    
    # Check app integrations
    try:
        from app_integrations import (
            finder_open_location, mail_compose_email,
            calendar_create_event, notes_create_note
        )
        capabilities["app_integrations"]["status"] = "available"
        capabilities["app_integrations"]["features"] = [
            "Finder integration",
            "Mail integration",
            "Calendar integration",
            "Notes integration",
            "System utilities"
        ]
    except ImportError as e:
        capabilities["app_integrations"]["status"] = "unavailable"
        capabilities["app_integrations"]["error"] = str(e)
    
    # Check learning system
    try:
        from learning_system import (
            remember_preference, recall_preference,
            get_command_patterns, get_recent_activity
        )
        capabilities["learning_system"]["status"] = "available"
        capabilities["learning_system"]["features"] = [
            "Preference memory",
            "Command pattern learning",
            "Activity tracking",
            "Context storage"
        ]
    except ImportError as e:
        capabilities["learning_system"]["status"] = "unavailable"
        capabilities["learning_system"]["error"] = str(e)
    
    # Check data analysis
    try:
        from data_analysis import (
            analyze_csv_file, analyze_json_file,
            analyze_directory_structure
        )
        capabilities["data_analysis"]["status"] = "available"
        capabilities["data_analysis"]["features"] = [
            "CSV analysis",
            "JSON processing",
            "Directory analysis",
            "Duplicate file detection"
        ]
    except ImportError as e:
        capabilities["data_analysis"]["status"] = "unavailable"
        capabilities["data_analysis"]["error"] = str(e)
    
    # Check voice recognition
    try:
        import whisper
        import sounddevice
        import soundfile
        capabilities["voice_recognition"]["status"] = "available"
        capabilities["voice_recognition"]["features"] = [
            "Whisper speech-to-text",
            "Audio recording",
            "Real-time transcription"
        ]
    except ImportError as e:
        capabilities["voice_recognition"]["status"] = "unavailable"
        capabilities["voice_recognition"]["error"] = str(e)
    
    # Check macOS integration
    try:
        import platform
        if platform.system() == "Darwin":
            from keychain_manager import KeychainManager
            capabilities["macos_integration"]["status"] = "available"
            capabilities["macos_integration"]["features"] = [
                "Keychain API key storage",
                "AppleScript automation",
                "macOS app control"
            ]
        else:
            capabilities["macos_integration"]["status"] = "unavailable"
            capabilities["macos_integration"]["error"] = "Not running on macOS"
    except ImportError as e:
        capabilities["macos_integration"]["status"] = "unavailable"
        capabilities["macos_integration"]["error"] = str(e)
    
    return capabilities


def format_capabilities_report(capabilities: Dict) -> str:
    """
    Format capabilities dictionary into a readable report.
    
    Args:
        capabilities: Capabilities dictionary from check_atom_capabilities()
        
    Returns:
        Formatted string report
    """
    lines = ["Atom AI Assistant - Capability Report", "=" * 50, ""]
    
    for category, info in capabilities.items():
        status_icon = "✅" if info["status"] == "available" else "❌"
        category_name = category.replace("_", " ").title()
        
        lines.append(f"{status_icon} {category_name}: {info['status'].upper()}")
        
        if info["status"] == "available" and info.get("features"):
            for feature in info["features"]:
                lines.append(f"   • {feature}")
        elif info["status"] == "unavailable" and info.get("error"):
            lines.append(f"   Error: {info['error']}")
        
        lines.append("")
    
    return "\n".join(lines)


def run_full_diagnostics() -> Dict:
    """
    Run full diagnostics including API validation and capability checking.
    
    Returns:
        Dictionary with all diagnostic results
    """
    print("\n🔍 Running Atom AI Assistant Diagnostics...\n")
    
    # Check API key
    print("📡 Testing OpenAI API key...")
    api_valid, api_message = validate_openai_api_key()
    print(f"   {'✅' if api_valid else '❌'} {api_message}\n")
    
    # Check capabilities
    print("⚙️  Checking system capabilities...")
    capabilities = check_atom_capabilities()
    
    results = {
        "api_key_valid": api_valid,
        "api_key_message": api_message,
        "capabilities": capabilities
    }
    
    # Print formatted report
    print(format_capabilities_report(capabilities))
    
    # Summary
    available_count = sum(1 for c in capabilities.values() if c["status"] == "available")
    total_count = len(capabilities)
    
    print(f"\n📊 Summary: {available_count}/{total_count} capability areas available")
    print(f"🔑 API Key Status: {'✅ Valid' if api_valid else '❌ Invalid'}")
    
    return results


if __name__ == "__main__":
    # Run diagnostics when executed directly
    results = run_full_diagnostics()
    
    # Exit with appropriate code
    if not results["api_key_valid"]:
        print("\n⚠️  Warning: API key is not valid. Please configure your OpenAI API key.")
        print("Run: python keychain_manager.py")
        sys.exit(1)
    
    unavailable = [k for k, v in results["capabilities"].items() if v["status"] == "unavailable"]
    if unavailable:
        print(f"\n⚠️  Some capabilities are unavailable: {', '.join(unavailable)}")
        print("Install missing dependencies with: pip install -r requirements.txt")
    
    sys.exit(0)
