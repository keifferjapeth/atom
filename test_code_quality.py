#!/usr/bin/env python3
"""
Simple code quality tests that don't require imports.
Tests that the performance improvements are correctly implemented.
"""

import ast
import re
import sys


def test_gui_whisper_caching():
    """Test that GUI code has Whisper model caching."""
    print("🧪 Testing Whisper model caching in GUI...")
    
    with open('gui.py', 'r') as f:
        gui_code = f.read()
    
    checks = [
        ('whisper_model = None' in gui_code, 'Model cache variable defined'),
        ('if self.whisper_model is None:' in gui_code, 'Model cache check present'),
        ('self.whisper_model = whisper.load_model' in gui_code, 'Model cached on first load'),
        ('self.whisper_model.transcribe' in gui_code, 'Using cached model for transcription'),
    ]
    
    all_passed = True
    for check, description in checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description} - NOT FOUND")
            all_passed = False
    
    return all_passed


def test_database_indexes():
    """Test that database initialization creates indexes."""
    print("\n🧪 Testing database index creation...")
    
    with open('learning_system.py', 'r') as f:
        code = f.read()
    
    expected_indexes = [
        'idx_command_history_timestamp',
        'idx_command_history_type',
        'idx_user_preferences_category',
        'idx_learned_patterns_type',
        'idx_learned_patterns_confidence',
        'idx_location_preferences_context',
        'idx_conversation_context_session',
    ]
    
    all_passed = True
    for index_name in expected_indexes:
        if index_name in code:
            print(f"  ✅ Index '{index_name}' created")
        else:
            print(f"  ❌ Index '{index_name}' NOT FOUND")
            all_passed = False
    
    return all_passed


def test_file_hash_optimization():
    """Test that file hash uses optimized chunk size."""
    print("\n🧪 Testing file hash optimization...")
    
    with open('data_analysis.py', 'r') as f:
        code = f.read()
    
    # Look for the get_file_hash function
    if 'def get_file_hash' in code:
        print("  ✅ get_file_hash function found")
        
        # Check for optimized chunk size (should be 64KB = 65536)
        if 'chunk_size: int = 65536' in code or 'chunk_size=65536' in code:
            print("  ✅ Using optimized chunk size (64KB)")
            return True
        else:
            print("  ⚠️  Chunk size may not be optimized")
            return False
    else:
        print("  ❌ get_file_hash function NOT FOUND")
        return False


def test_directory_analysis_limits():
    """Test that directory analysis has memory limits."""
    print("\n🧪 Testing directory analysis memory limits...")
    
    with open('data_analysis.py', 'r') as f:
        code = f.read()
    
    checks = [
        ('MAX_TRACKED_FILES' in code, 'MAX_TRACKED_FILES constant defined'),
        ('if files_processed >= MAX_TRACKED_FILES:' in code, 'File limit check present'),
        ('len(stats[\'largest_files\']) < 10' in code or 'len(stats["largest_files"]) < 10' in code, 
         'Memory-efficient tracking of largest files'),
    ]
    
    all_passed = True
    for check, description in checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description} - NOT FOUND")
            all_passed = False
    
    return all_passed


def test_gui_methods():
    """Test that GUI has all required methods."""
    print("\n🧪 Testing GUI method implementations...")
    
    with open('gui.py', 'r') as f:
        code = f.read()
    
    required_methods = [
        'on_run_command',
        'append_log',
        'refresh_insights',
    ]
    
    all_passed = True
    for method in required_methods:
        if f'def {method}' in code:
            print(f"  ✅ Method '{method}' implemented")
        else:
            print(f"  ❌ Method '{method}' NOT FOUND")
            all_passed = False
    
    return all_passed


def test_syntax_validity():
    """Test that all modified files have valid Python syntax."""
    print("\n🧪 Testing Python syntax validity...")
    
    files = ['gui.py', 'data_analysis.py', 'learning_system.py']
    all_passed = True
    
    for filename in files:
        try:
            with open(filename, 'r') as f:
                ast.parse(f.read())
            print(f"  ✅ {filename} - valid syntax")
        except SyntaxError as e:
            print(f"  ❌ {filename} - syntax error: {e}")
            all_passed = False
    
    return all_passed


def main():
    """Run all tests."""
    print("=" * 60)
    print("Atom AI Performance Improvements - Code Quality Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_syntax_validity,
        test_gui_whisper_caching,
        test_database_indexes,
        test_file_hash_optimization,
        test_directory_analysis_limits,
        test_gui_methods,
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Test {test_func.__name__} crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total} tests")
    
    if passed == total:
        print("\n✅ All tests passed! Performance improvements verified.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
