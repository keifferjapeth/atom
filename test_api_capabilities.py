#!/usr/bin/env python3
"""
Test script for API validation and capability checking.
This script can be run to test all API keys and check Atom capabilities.
"""
import sys
import os
from api_validator import (
    validate_openai_api_key,
    check_atom_capabilities,
    format_capabilities_report,
    run_full_diagnostics
)


def test_api_key_validation():
    """Test OpenAI API key validation."""
    print("\n" + "=" * 60)
    print("Testing API Key Validation")
    print("=" * 60)
    
    # Test with no API key
    print("\n1. Testing with no API key:")
    is_valid, message = validate_openai_api_key("")
    print(f"   Result: {message}")
    assert not is_valid, "Empty API key should be invalid"
    
    # Test with invalid format
    print("\n2. Testing with invalid format:")
    is_valid, message = validate_openai_api_key("invalid-key")
    print(f"   Result: {message}")
    assert not is_valid, "Invalid format should be rejected"
    
    # Test with current API key (if available)
    print("\n3. Testing with current API key:")
    try:
        from keychain_manager import get_openai_api_key_with_fallback
        api_key = get_openai_api_key_with_fallback()
        if api_key:
            is_valid, message = validate_openai_api_key(api_key)
            print(f"   Result: {message}")
            if is_valid:
                print("   ✅ API key is valid!")
            else:
                print(f"   ⚠️  API key issue: {message}")
        else:
            print("   ⚠️  No API key configured")
    except ImportError as e:
        print(f"   ⚠️  Cannot test: Missing dependency ({e})")
    except Exception as e:
        print(f"   ⚠️  Cannot test: {e}")
    
    print("\n✅ API key validation tests completed")


def test_capability_checking():
    """Test capability checking functionality."""
    print("\n" + "=" * 60)
    print("Testing Capability Checking")
    print("=" * 60)
    
    capabilities = check_atom_capabilities()
    
    print("\nCapability Summary:")
    for category, info in capabilities.items():
        status_icon = "✅" if info["status"] == "available" else "❌"
        print(f"{status_icon} {category.replace('_', ' ').title()}: {info['status']}")
        
        if info.get("features"):
            print(f"   Features: {', '.join(info['features'])}")
        if info.get("error"):
            print(f"   Error: {info['error']}")
    
    print("\n✅ Capability checking tests completed")
    
    return capabilities


def test_formatted_report():
    """Test the formatted capabilities report."""
    print("\n" + "=" * 60)
    print("Testing Formatted Report Generation")
    print("=" * 60)
    
    capabilities = check_atom_capabilities()
    report = format_capabilities_report(capabilities)
    
    print("\n" + report)
    
    print("\n✅ Report generation test completed")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("ATOM AI ASSISTANT - API & CAPABILITY TESTS")
    print("=" * 60)
    
    try:
        # Test API key validation
        test_api_key_validation()
        
        # Test capability checking
        capabilities = test_capability_checking()
        
        # Test formatted report
        test_formatted_report()
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        available_count = sum(1 for c in capabilities.values() if c["status"] == "available")
        total_count = len(capabilities)
        
        print(f"\n✅ All tests completed successfully!")
        print(f"📊 System Status: {available_count}/{total_count} capabilities available")
        
        # Check if critical components are available
        critical_missing = []
        if capabilities["core"]["status"] != "available":
            critical_missing.append("Core functionality")
        
        if critical_missing:
            print(f"\n⚠️  Critical components missing: {', '.join(critical_missing)}")
            print("   Install dependencies: pip install -r requirements.txt")
            return 1
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
