"""
Advanced Data Analysis Tools for Atom AI Assistant.
Provides comprehensive data analysis capabilities for various file formats and data sources.
"""

import json
import csv
import os
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import xml.etree.ElementTree as ET
import subprocess
from collections import Counter, defaultdict
from langchain.agents import tool


# ============================================================================
# CSV DATA ANALYSIS
# ============================================================================

@tool
def analyze_csv_file(file_path: str, show_sample: bool = True):
    """
    Analyze a CSV file and provide comprehensive statistics and insights.
    
    Args:
        file_path: Path to the CSV file
        show_sample: Whether to show sample data
        
    Returns:
        Detailed analysis of the CSV file
    """
    try:
        file_path = os.path.expanduser(file_path)
        
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"
        
        # Read CSV with pandas for advanced analysis
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            return f"❌ Error reading CSV: {str(e)}"
        
        analysis = f"📊 CSV Analysis: {os.path.basename(file_path)}\\n"
        analysis += "=" * 50 + "\\n\\n"
        
        # Basic info
        rows, cols = df.shape
        analysis += f"📐 Dimensions: {rows} rows × {cols} columns\\n"
        analysis += f"💾 File size: {format_file_size(os.path.getsize(file_path))}\\n\\n"
        
        # Column information
        analysis += "📋 Column Information:\\n"
        for i, col in enumerate(df.columns):
            dtype = df[col].dtype
            null_count = df[col].isnull().sum()
            unique_count = df[col].nunique()
            analysis += f"  {i+1:2d}. {col:20s} | Type: {str(dtype):10s} | Nulls: {null_count:6d} | Unique: {unique_count}\\n"
        
        # Sample data
        if show_sample and rows > 0:
            analysis += "\\n📄 Sample Data (First 3 rows):\\n"
            sample = df.head(3).to_string(max_cols=8, max_colwidth=20)
            analysis += sample + "\\n"
        
        # Statistical summary for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            analysis += "\\n📈 Numeric Summary:\\n"
            stats = df[numeric_cols].describe()
            analysis += stats.to_string() + "\\n"
        
        # Missing data analysis
        missing = df.isnull().sum()
        missing_cols = missing[missing > 0]
        if len(missing_cols) > 0:
            analysis += "\\n⚠️  Missing Data:\\n"
            for col, count in missing_cols.items():
                percentage = (count / rows) * 100
                analysis += f"  • {col}: {count} ({percentage:.1f}%)\\n"
        
        return analysis
        
    except Exception as e:
        return f"❌ Error analyzing CSV: {str(e)}"

@tool
def csv_query(file_path: str, query_description: str):
    """
    Query CSV data using natural language description.
    
    Args:
        file_path: Path to the CSV file
        query_description: Natural language description of what to find
        
    Returns:
        Query results based on the description
    """
    try:
        file_path = os.path.expanduser(file_path)
        df = pd.read_csv(file_path)
        
        # Simple query patterns - can be extended with more sophisticated NLP
        query_lower = query_description.lower()
        
        result = f"🔍 Query: {query_description}\\n"
        result += f"📊 File: {os.path.basename(file_path)}\\n\\n"
        
        if "average" in query_lower or "mean" in query_lower:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                result += "📊 Average values:\\n"
                for col in numeric_cols:
                    avg = df[col].mean()
                    result += f"  • {col}: {avg:.2f}\\n"
            else:
                result += "No numeric columns for average calculation.\\n"
        
        elif "max" in query_lower or "maximum" in query_lower:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                result += "📈 Maximum values:\\n"
                for col in numeric_cols:
                    max_val = df[col].max()
                    result += f"  • {col}: {max_val}\\n"
        
        elif "count" in query_lower:
            result += f"📊 Row count: {len(df)}\\n"
            result += f"📋 Column count: {len(df.columns)}\\n"
            
            # Count unique values in categorical columns
            cat_cols = df.select_dtypes(include=['object']).columns
            if len(cat_cols) > 0:
                result += "\\n🏷️  Unique value counts:\\n"
                for col in cat_cols[:5]:  # Limit to first 5 columns
                    unique_count = df[col].nunique()
                    result += f"  • {col}: {unique_count} unique values\\n"
        
        elif "null" in query_lower or "missing" in query_lower:
            missing = df.isnull().sum()
            missing_cols = missing[missing > 0]
            if len(missing_cols) > 0:
                result += "⚠️  Missing data:\\n"
                for col, count in missing_cols.items():
                    percentage = (count / len(df)) * 100
                    result += f"  • {col}: {count} ({percentage:.1f}%)\\n"
            else:
                result += "✅ No missing data found.\\n"
        
        else:
            # Default: show basic info
            result += f"📊 Basic information:\\n"
            result += f"  • Rows: {len(df)}\\n"
            result += f"  • Columns: {len(df.columns)}\\n"
            result += f"  • Columns: {', '.join(df.columns[:8])}{'...' if len(df.columns) > 8 else ''}\\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error querying CSV: {str(e)}"


# ============================================================================
# JSON DATA ANALYSIS
# ============================================================================

@tool
def analyze_json_file(file_path: str, max_depth: int = 3):
    """
    Analyze a JSON file structure and content.
    
    Args:
        file_path: Path to the JSON file
        max_depth: Maximum depth to analyze in nested structures
        
    Returns:
        Detailed JSON structure analysis
    """
    try:
        file_path = os.path.expanduser(file_path)
        
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        analysis = f"🔧 JSON Analysis: {os.path.basename(file_path)}\\n"
        analysis += "=" * 50 + "\\n\\n"
        
        # File info
        file_size = os.path.getsize(file_path)
        analysis += f"💾 File size: {format_file_size(file_size)}\\n"
        analysis += f"🏗️  Root type: {type(data).__name__}\\n\\n"
        
        # Analyze structure
        structure_info = analyze_json_structure(data, max_depth)
        analysis += "🌳 Structure Analysis:\\n"
        analysis += structure_info + "\\n"
        
        # Statistics
        stats = get_json_statistics(data)
        if stats:
            analysis += "📊 Statistics:\\n"
            analysis += f"  • Total keys: {stats.get('total_keys', 0)}\\n"
            analysis += f"  • Max depth: {stats.get('max_depth', 0)}\\n"
            analysis += f"  • Arrays found: {stats.get('array_count', 0)}\\n"
            analysis += f"  • Objects found: {stats.get('object_count', 0)}\\n\\n"
        
        # Sample data for arrays/objects
        if isinstance(data, (list, dict)):
            sample = get_json_sample(data, max_items=3)
            if sample:
                analysis += "📄 Sample Content:\\n"
                analysis += json.dumps(sample, indent=2, ensure_ascii=False)[:500]
                if len(str(data)) > 500:
                    analysis += "\\n... (truncated)"
        
        return analysis
        
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON format: {str(e)}"
    except Exception as e:
        return f"❌ Error analyzing JSON: {str(e)}"

@tool
def json_extract_keys(file_path: str, key_pattern: str = None):
    """
    Extract and list all keys from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        key_pattern: Optional pattern to filter keys (contains match)
        
    Returns:
        List of keys found in the JSON structure
    """
    try:
        file_path = os.path.expanduser(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        all_keys = extract_all_keys(data)
        
        if key_pattern:
            filtered_keys = [key for key in all_keys if key_pattern.lower() in key.lower()]
            result = f"🔑 Keys matching '{key_pattern}' in {os.path.basename(file_path)}:\\n"
            if filtered_keys:
                for key in sorted(filtered_keys):
                    result += f"  • {key}\\n"
            else:
                result += f"  No keys found matching '{key_pattern}'\\n"
        else:
            result = f"🔑 All keys in {os.path.basename(file_path)} ({len(all_keys)} total):\\n"
            for key in sorted(all_keys)[:50]:  # Limit to first 50
                result += f"  • {key}\\n"
            if len(all_keys) > 50:
                result += f"  ... and {len(all_keys) - 50} more keys\\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error extracting keys: {str(e)}"


# ============================================================================
# DIRECTORY AND FILE SYSTEM ANALYSIS
# ============================================================================

@tool
def analyze_directory_structure(directory_path: str, max_depth: int = 3, include_hidden: bool = False):
    """
    Analyze directory structure and provide insights about file organization.
    
    Args:
        directory_path: Path to analyze
        max_depth: Maximum depth to traverse
        include_hidden: Whether to include hidden files/directories
        
    Returns:
        Directory structure analysis
    """
    try:
        directory_path = os.path.expanduser(directory_path)
        
        if not os.path.exists(directory_path):
            return f"❌ Directory not found: {directory_path}"
        
        if not os.path.isdir(directory_path):
            return f"❌ Not a directory: {directory_path}"
        
        analysis = f"📁 Directory Analysis: {os.path.basename(directory_path)}\\n"
        analysis += "=" * 50 + "\\n\\n"
        
        # Collect statistics
        stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'file_types': Counter(),
            'largest_files': [],
            'oldest_files': [],
            'newest_files': []
        }
        
        # Limit memory by not keeping all file info in memory
        MAX_TRACKED_FILES = 1000
        files_processed = 0
        
        # Walk through directory
        for root, dirs, files in os.walk(directory_path):
            # Check depth
            depth = root.replace(directory_path, '').count(os.sep)
            if depth >= max_depth:
                dirs[:] = []  # Don't recurse further
                continue
            
            # Filter hidden files/dirs if needed
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                files = [f for f in files if not f.startswith('.')]
            
            stats['total_dirs'] += len(dirs)
            
            for file in files:
                # Limit processing to avoid memory issues
                if files_processed >= MAX_TRACKED_FILES:
                    break
                    
                file_path = os.path.join(root, file)
                try:
                    stat_info = os.stat(file_path)
                    file_size = stat_info.st_size
                    mtime = stat_info.st_mtime
                    
                    stats['total_files'] += 1
                    stats['total_size'] += file_size
                    
                    # File extension
                    _, ext = os.path.splitext(file)
                    if ext:
                        stats['file_types'][ext.lower()] += 1
                    else:
                        stats['file_types']['[no extension]'] += 1
                    
                    # Track largest files (keep only top 10)
                    file_info = (file_path, file_size, mtime)
                    if len(stats['largest_files']) < 10:
                        stats['largest_files'].append(file_info)
                        stats['largest_files'].sort(key=lambda x: x[1], reverse=True)
                    elif file_size > stats['largest_files'][-1][1]:
                        stats['largest_files'][-1] = file_info
                        stats['largest_files'].sort(key=lambda x: x[1], reverse=True)
                    
                    # Track oldest files (keep only top 5)
                    if len(stats['oldest_files']) < 5:
                        stats['oldest_files'].append(file_info)
                        stats['oldest_files'].sort(key=lambda x: x[2])
                    elif mtime < stats['oldest_files'][-1][2]:
                        stats['oldest_files'][-1] = file_info
                        stats['oldest_files'].sort(key=lambda x: x[2])
                    
                    # Track newest files (keep only top 5)
                    if len(stats['newest_files']) < 5:
                        stats['newest_files'].append(file_info)
                        stats['newest_files'].sort(key=lambda x: x[2], reverse=True)
                    elif mtime > stats['newest_files'][-1][2]:
                        stats['newest_files'][-1] = file_info
                        stats['newest_files'].sort(key=lambda x: x[2], reverse=True)
                    
                    files_processed += 1
                    
                except (OSError, IOError):
                    continue
            
            if files_processed >= MAX_TRACKED_FILES:
                analysis += f"⚠️  Processing limited to {MAX_TRACKED_FILES} files for performance\\n\\n"
                break
        
        # Generate report
        analysis += f"📊 Summary:\\n"
        analysis += f"  • Total files: {stats['total_files']:,}\\n"
        analysis += f"  • Total directories: {stats['total_dirs']:,}\\n"
        analysis += f"  • Total size: {format_file_size(stats['total_size'])}\\n\\n"
        
        # File types
        if stats['file_types']:
            analysis += "📋 File Types:\\n"
            for ext, count in stats['file_types'].most_common(10):
                percentage = (count / stats['total_files']) * 100
                analysis += f"  • {ext:15s}: {count:6,} files ({percentage:5.1f}%)\\n"
            analysis += "\\n"
        
        # Largest files
        if stats['largest_files']:
            analysis += "💾 Largest Files:\\n"
            for file_path, size, _ in stats['largest_files']:
                rel_path = os.path.relpath(file_path, directory_path)
                analysis += f"  • {format_file_size(size):>10s}: {rel_path}\\n"
            analysis += "\\n"
        
        # Newest files
        if stats['newest_files']:
            analysis += "🆕 Newest Files:\\n"
            for file_path, _, mtime in stats['newest_files']:
                rel_path = os.path.relpath(file_path, directory_path)
                date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                analysis += f"  • {date_str}: {rel_path}\\n"
        
        return analysis
        
    except Exception as e:
        return f"❌ Error analyzing directory: {str(e)}"

@tool
def find_duplicate_files(directory_path: str, min_size: int = 1024):
    """
    Find duplicate files in a directory based on file size and content.
    
    Args:
        directory_path: Directory to search for duplicates
        min_size: Minimum file size to consider (bytes)
        
    Returns:
        List of duplicate files found
    """
    try:
        directory_path = os.path.expanduser(directory_path)
        
        if not os.path.exists(directory_path):
            return f"❌ Directory not found: {directory_path}"
        
        # Dictionary to store file hashes
        size_groups = defaultdict(list)
        hash_groups = defaultdict(list)
        
        # First pass: group by size
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    if size >= min_size:
                        size_groups[size].append(file_path)
                except (OSError, IOError):
                    continue
        
        # Second pass: hash files with same size
        duplicates_found = []
        total_duplicate_size = 0
        
        for size, file_list in size_groups.items():
            if len(file_list) > 1:  # Only check files with same size
                for file_path in file_list:
                    try:
                        file_hash = get_file_hash(file_path)
                        hash_groups[file_hash].append((file_path, size))
                    except Exception:
                        continue
        
        # Find actual duplicates (same hash)
        for file_hash, file_list in hash_groups.items():
            if len(file_list) > 1:
                duplicates_found.append(file_list)
                # Calculate size saved if duplicates were removed (keep one)
                total_duplicate_size += file_list[0][1] * (len(file_list) - 1)
        
        # Generate report
        if duplicates_found:
            result = f"🔍 Duplicate Files in {os.path.basename(directory_path)}:\\n"
            result += "=" * 50 + "\\n\\n"
            result += f"📊 Summary: {len(duplicates_found)} groups of duplicates found\\n"
            result += f"💾 Potential space savings: {format_file_size(total_duplicate_size)}\\n\\n"
            
            for i, group in enumerate(duplicates_found, 1):
                file_size = group[0][1]
                result += f"Group {i} - Size: {format_file_size(file_size)}\\n"
                for file_path, _ in group:
                    rel_path = os.path.relpath(file_path, directory_path)
                    result += f"  • {rel_path}\\n"
                result += "\\n"
                
                # Limit output to prevent overwhelming
                if i >= 20:
                    remaining = len(duplicates_found) - 20
                    if remaining > 0:
                        result += f"... and {remaining} more duplicate groups\\n"
                    break
        else:
            result = f"✅ No duplicate files found in {os.path.basename(directory_path)}"
        
        return result
        
    except Exception as e:
        return f"❌ Error finding duplicates: {str(e)}"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_file_size(size_bytes: int) -> str:
    """Convert bytes to human-readable file size."""
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.1f} {units[unit_index]}"

def analyze_json_structure(data, max_depth=3, current_depth=0):
    """Recursively analyze JSON structure."""
    if current_depth >= max_depth:
        return "  [Max depth reached]\\n"
    
    result = ""
    indent = "  " * current_depth
    
    if isinstance(data, dict):
        result += f"{indent}Object ({len(data)} keys):\\n"
        for key, value in list(data.items())[:5]:  # Limit to first 5 keys
            result += f"{indent}  {key}: {type(value).__name__}\\n"
            if isinstance(value, (dict, list)) and current_depth < max_depth - 1:
                result += analyze_json_structure(value, max_depth, current_depth + 2)
        if len(data) > 5:
            result += f"{indent}  ... and {len(data) - 5} more keys\\n"
    
    elif isinstance(data, list):
        result += f"{indent}Array ({len(data)} items)\\n"
        if data:
            first_item = data[0]
            result += f"{indent}  Item type: {type(first_item).__name__}\\n"
            if isinstance(first_item, (dict, list)) and current_depth < max_depth - 1:
                result += analyze_json_structure(first_item, max_depth, current_depth + 1)
    
    return result

def get_json_statistics(data):
    """Get statistics from JSON data."""
    stats = {
        'total_keys': 0,
        'max_depth': 0,
        'array_count': 0,
        'object_count': 0
    }
    
    def count_recursive(obj, depth=0):
        stats['max_depth'] = max(stats['max_depth'], depth)
        
        if isinstance(obj, dict):
            stats['object_count'] += 1
            stats['total_keys'] += len(obj)
            for value in obj.values():
                count_recursive(value, depth + 1)
        
        elif isinstance(obj, list):
            stats['array_count'] += 1
            for item in obj:
                count_recursive(item, depth + 1)
    
    count_recursive(data)
    return stats

def get_json_sample(data, max_items=3):
    """Get a sample of JSON data."""
    if isinstance(data, dict):
        keys = list(data.keys())[:max_items]
        return {key: data[key] for key in keys}
    elif isinstance(data, list):
        return data[:max_items]
    else:
        return data

def extract_all_keys(obj, keys=None, path=""):
    """Extract all keys from nested JSON structure."""
    if keys is None:
        keys = set()
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            full_key = f"{path}.{key}" if path else key
            keys.add(full_key)
            extract_all_keys(value, keys, full_key)
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            extract_all_keys(item, keys, f"{path}[{i}]" if path else f"[{i}]")
    
    return keys

def get_file_hash(file_path: str, chunk_size: int = 65536) -> str:
    """Calculate MD5 hash of a file efficiently with optimized chunk size."""
    import hashlib
    hash_md5 = hashlib.md5()
    
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)
    
    return hash_md5.hexdigest()