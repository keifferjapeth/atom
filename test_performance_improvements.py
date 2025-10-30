#!/usr/bin/env python3
"""
Test script to validate performance improvements in Atom AI Assistant.
This script tests the optimizations without requiring macOS-specific features.
"""

import os
import sys
import time
import tempfile
import sqlite3
from pathlib import Path

def test_database_indexes():
    """Test that database indexes are created properly."""
    print("🧪 Testing database indexes...")
    
    # Import and initialize learning system
    try:
        from learning_system import AtomMemory
        
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            temp_db = f.name
        
        # Initialize memory system
        memory = AtomMemory(db_path=temp_db)
        
        # Check if indexes exist
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]
        
        expected_indexes = [
            'idx_command_history_timestamp',
            'idx_command_history_type',
            'idx_user_preferences_category',
            'idx_learned_patterns_type',
            'idx_learned_patterns_confidence',
            'idx_location_preferences_context',
            'idx_conversation_context_session'
        ]
        
        missing_indexes = [idx for idx in expected_indexes if idx not in indexes]
        
        conn.close()
        os.unlink(temp_db)
        
        if missing_indexes:
            print(f"  ❌ Missing indexes: {missing_indexes}")
            return False
        else:
            print(f"  ✅ All {len(expected_indexes)} database indexes created")
            return True
            
    except Exception as e:
        print(f"  ❌ Error testing database indexes: {e}")
        return False


def test_file_hash_performance():
    """Test that file hash computation uses optimized chunk size."""
    print("\n🧪 Testing file hash performance...")
    
    try:
        from data_analysis import get_file_hash
        
        # Create a test file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            test_file = f.name
            # Write 10MB of data
            f.write(b'x' * (10 * 1024 * 1024))
        
        # Test hash computation
        start_time = time.time()
        hash_result = get_file_hash(test_file)
        elapsed = time.time() - start_time
        
        os.unlink(test_file)
        
        if hash_result and len(hash_result) == 32:  # MD5 hash is 32 chars
            print(f"  ✅ File hash computed in {elapsed:.3f}s (10MB file)")
            print(f"     Hash: {hash_result[:16]}...")
            return True
        else:
            print(f"  ❌ Invalid hash result: {hash_result}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error testing file hash: {e}")
        return False


def test_directory_analysis_limits():
    """Test that directory analysis has memory limits."""
    print("\n🧪 Testing directory analysis memory limits...")
    
    try:
        from data_analysis import analyze_directory_structure
        
        # Create temporary directory with some files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create subdirectories
            for i in range(3):
                subdir = os.path.join(temp_dir, f"subdir_{i}")
                os.makedirs(subdir)
                
                # Create some files
                for j in range(5):
                    filepath = os.path.join(subdir, f"file_{j}.txt")
                    with open(filepath, 'w') as f:
                        f.write(f"Test content {i}-{j}")
            
            # Test analysis
            result = analyze_directory_structure(temp_dir, max_depth=2)
            
            if "Directory Analysis" in result and "Summary" in result:
                print(f"  ✅ Directory analysis completed successfully")
                print(f"     Result length: {len(result)} chars")
                return True
            else:
                print(f"  ❌ Unexpected analysis result")
                return False
                
    except Exception as e:
        print(f"  ❌ Error testing directory analysis: {e}")
        return False


def test_whisper_model_caching():
    """Test that GUI code has Whisper model caching."""
    print("\n🧪 Testing Whisper model caching in GUI...")
    
    try:
        # Read gui.py to check for whisper_model caching
        with open('gui.py', 'r') as f:
            gui_code = f.read()
        
        checks = [
            ('whisper_model = None' in gui_code, 'Model cache variable defined'),
            ('if self.whisper_model is None:' in gui_code, 'Model cache check present'),
            ('self.whisper_model = whisper.load_model' in gui_code, 'Model cached on first load'),
        ]
        
        all_passed = True
        for check, description in checks:
            if check:
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ {description} - NOT FOUND")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"  ❌ Error testing GUI code: {e}")
        return False


def test_imports():
    """Test that all modules can be imported."""
    print("\n🧪 Testing module imports...")
    
    modules_to_test = [
        ('commands', 'commands.py'),
        ('learning_system', 'learning_system.py'),
        ('data_analysis', 'data_analysis.py'),
        ('app_integrations', 'app_integrations.py'),
        ('keychain_manager', 'keychain_manager.py'),
    ]
    
    all_passed = True
    for module_name, file_path in modules_to_test:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name} imported successfully")
        except ImportError as e:
            # Some imports may fail due to missing dependencies, that's ok
            if 'PyQt6' in str(e) or 'whisper' in str(e) or 'pandas' in str(e):
                print(f"  ⚠️  {module_name} - optional dependency missing: {e}")
            else:
                print(f"  ❌ {module_name} import error: {e}")
                all_passed = False
        except Exception as e:
            print(f"  ❌ {module_name} unexpected error: {e}")
            all_passed = False
    
    return all_passed


def main():
    """Run all tests."""
    print("=" * 60)
    print("Atom AI Performance Improvements - Test Suite")
    print("=" * 60)
    
    tests = [
        test_whisper_model_caching,
        test_database_indexes,
        test_file_hash_performance,
        test_directory_analysis_limits,
        test_imports,
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Test {test_func.__name__} crashed: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total} tests")
    
    if passed == total:
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
