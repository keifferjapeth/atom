#!/usr/bin/env python3
"""
Atom AI Assistant Setup and Diagnostic Tool
Checks macOS/Xcode environment, validates API keys, and ensures all capabilities work.
"""
import sys
import os
import platform
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def check_python_version():
    """Check if Python version is compatible."""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 10:
        print("✅ Python version is compatible (3.10+)")
        return True
    else:
        print("❌ Python 3.10 or higher is required")
        return False


def check_macos_environment():
    """Check if running on macOS and verify Xcode tools."""
    print_header("Checking macOS Environment")
    
    system = platform.system()
    print(f"Operating System: {system}")
    
    if system != "Darwin":
        print("⚠️  Not running on macOS. Some features may not be available.")
        return False
    
    print("✅ Running on macOS")
    
    # Check for Xcode command line tools
    print("\nChecking for Xcode Command Line Tools...")
    try:
        result = subprocess.run(
            ["xcode-select", "-p"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ Xcode tools installed at: {result.stdout.strip()}")
            
            # Check clang (part of Xcode)
            try:
                clang_result = subprocess.run(
                    ["clang", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if clang_result.returncode == 0:
                    print("✅ Clang compiler available")
            except Exception:
                pass
            
            return True
        else:
            print("❌ Xcode command line tools not found")
            print("   Install with: xcode-select --install")
            return False
    except FileNotFoundError:
        print("❌ xcode-select not found")
        return False
    except Exception as e:
        print(f"⚠️  Could not check Xcode tools: {e}")
        return False


def check_ffmpeg():
    """Check if FFmpeg is installed."""
    print_header("Checking FFmpeg")
    
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Extract version from first line
            first_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg installed: {first_line}")
            return True
        else:
            print("❌ FFmpeg not working properly")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found")
        print("   Install with: brew install ffmpeg")
        return False
    except Exception as e:
        print(f"❌ Error checking FFmpeg: {e}")
        return False


def check_dependencies():
    """Check if Python dependencies are installed."""
    print_header("Checking Python Dependencies")
    
    required_packages = [
        ("openai", "openai"),
        ("whisper", "openai-whisper"),
        ("langchain", "langchain"),
        ("PyQt6", "PyQt6"),
        ("sounddevice", "sounddevice"),
        ("soundfile", "soundfile"),
        ("numpy", "numpy"),
        ("dotenv", "python-dotenv"),
    ]
    
    all_installed = True
    
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - Not installed")
            all_installed = False
    
    if not all_installed:
        print("\n⚠️  Some dependencies are missing.")
        print("   Install with: pip install -r requirements.txt")
        print("   Or use Poetry: poetry install")
    
    return all_installed


def check_api_key():
    """Check if OpenAI API key is configured."""
    print_header("Checking OpenAI API Key")
    
    try:
        from api_validator import validate_openai_api_key
        
        is_valid, message = validate_openai_api_key()
        
        if is_valid:
            print(f"✅ {message}")
            return True
        else:
            print(f"❌ {message}")
            print("\n   Configure your API key using one of these methods:")
            print("   1. python keychain_manager.py (Recommended for macOS)")
            print("   2. export OPENAI_API_KEY='your-key-here'")
            print("   3. Create a .env file with: OPENAI_API_KEY=your-key-here")
            return False
    except Exception as e:
        print(f"⚠️  Cannot validate API key: {e}")
        return False


def check_capabilities():
    """Check Atom capabilities."""
    print_header("Checking Atom Capabilities")
    
    try:
        from api_validator import check_atom_capabilities
        
        capabilities = check_atom_capabilities()
        
        for category, info in capabilities.items():
            status_icon = "✅" if info["status"] == "available" else "❌"
            category_name = category.replace("_", " ").title()
            print(f"{status_icon} {category_name}")
            
            if info.get("features") and info["status"] == "available":
                for feature in info["features"][:3]:  # Show first 3 features
                    print(f"   • {feature}")
            elif info.get("error"):
                print(f"   Error: {info['error']}")
        
        available_count = sum(1 for c in capabilities.values() if c["status"] == "available")
        total_count = len(capabilities)
        
        print(f"\n📊 Summary: {available_count}/{total_count} capabilities available")
        
        return available_count > 0
        
    except Exception as e:
        print(f"⚠️  Cannot check capabilities: {e}")
        return False


def check_file_structure():
    """Verify that all required files are present."""
    print_header("Checking File Structure")
    
    required_files = [
        "main.py",
        "gui.py",
        "commands.py",
        "keychain_manager.py",
        "api_validator.py",
        "requirements.txt",
        "README.md",
        "assets/mic.svg",
        "assets/stop.svg",
    ]
    
    all_present = True
    base_path = Path(__file__).parent
    
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_present = False
    
    return all_present


def run_full_setup_check():
    """Run all setup checks and provide a comprehensive report."""
    print("\n" + "=" * 70)
    print("  ATOM AI ASSISTANT - XCODE ENVIRONMENT SETUP CHECK")
    print("=" * 70)
    
    results = {
        "python_version": check_python_version(),
        "macos_environment": check_macos_environment(),
        "ffmpeg": check_ffmpeg(),
        "dependencies": check_dependencies(),
        "api_key": check_api_key(),
        "capabilities": check_capabilities(),
        "file_structure": check_file_structure(),
    }
    
    # Final summary
    print_header("SETUP SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n✅ Passed: {passed}/{total} checks")
    
    if passed == total:
        print("\n🎉 All checks passed! Atom is ready to use.")
        print("\nTo start Atom:")
        print("   • GUI Mode: python gui.py")
        print("   • CLI Mode: python main.py 'your command here'")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please address the issues above.")
        
        if not results["macos_environment"]:
            print("\n📱 For best Xcode integration:")
            print("   • Install Xcode Command Line Tools: xcode-select --install")
            print("   • Ensure you're running on macOS for full functionality")
        
        if not results["dependencies"]:
            print("\n📦 To install dependencies:")
            print("   pip install -r requirements.txt")
        
        if not results["api_key"]:
            print("\n🔑 To configure API key:")
            print("   python keychain_manager.py")
        
        return 1


if __name__ == "__main__":
    exit_code = run_full_setup_check()
    sys.exit(exit_code)
