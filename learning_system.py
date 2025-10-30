"""
Atom AI Learning and Memory System.
Provides persistent memory, user pattern recognition, and adaptive behavior learning.
"""

import json
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter
import hashlib
from langchain.agents import tool


class AtomMemory:
    """Persistent memory system for Atom AI Assistant."""
    
    def __init__(self, db_path: str = None):
        """Initialize the memory system with SQLite database."""
        if db_path is None:
            # Store in user's home directory
            home_dir = os.path.expanduser("~")
            atom_dir = os.path.join(home_dir, ".atom_ai")
            os.makedirs(atom_dir, exist_ok=True)
            db_path = os.path.join(atom_dir, "atom_memory.db")
        
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Commands and interactions history
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    command TEXT NOT NULL,
                    command_type TEXT,
                    result TEXT,
                    success BOOLEAN,
                    execution_time REAL,
                    user_feedback TEXT
                )
            ''')
            
            # Add indexes for frequently-queried columns
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_command_history_timestamp 
                ON command_history(timestamp DESC)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_command_history_type 
                ON command_history(command_type)
            ''')
            
            # User preferences and settings
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    category TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_user_preferences_category 
                ON user_preferences(category)
            ''')
            
            # Learned patterns and behaviors
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learned_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT NOT NULL,
                    pattern_data TEXT NOT NULL,
                    confidence REAL DEFAULT 0.5,
                    usage_count INTEGER DEFAULT 1,
                    last_used DATETIME DEFAULT CURRENT_TIMESTAMP,
                    created DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_learned_patterns_type 
                ON learned_patterns(pattern_type)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_learned_patterns_confidence 
                ON learned_patterns(confidence DESC, usage_count DESC)
            ''')
            
            # File and location preferences
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS location_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    context TEXT NOT NULL,
                    preferred_path TEXT NOT NULL,
                    usage_count INTEGER DEFAULT 1,
                    last_used DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_location_preferences_context 
                ON location_preferences(context, usage_count DESC, last_used DESC)
            ''')
            
            # Conversation context
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversation_context (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    context_type TEXT,
                    context_data TEXT NOT NULL
                )
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_conversation_context_session 
                ON conversation_context(session_id, timestamp DESC)
            ''')
            
            conn.commit()
    
    def store_command(self, command: str, command_type: str = "general", 
                     result: str = "", success: bool = True, 
                     execution_time: float = 0.0):
        """Store a command execution in history."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO command_history 
                (command, command_type, result, success, execution_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (command, command_type, result, success, execution_time))
            conn.commit()
    
    def get_command_history(self, limit: int = 50, command_type: str = None) -> List[Dict]:
        """Retrieve command history."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if command_type:
                cursor.execute('''
                    SELECT * FROM command_history 
                    WHERE command_type = ? 
                    ORDER BY timestamp DESC LIMIT ?
                ''', (command_type, limit))
            else:
                cursor.execute('''
                    SELECT * FROM command_history 
                    ORDER BY timestamp DESC LIMIT ?
                ''', (limit,))
            
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def store_preference(self, key: str, value: str, category: str = "general"):
        """Store a user preference."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO user_preferences (key, value, category)
                VALUES (?, ?, ?)
            ''', (key, value, category))
            conn.commit()
    
    def get_preference(self, key: str) -> Optional[str]:
        """Get a user preference."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM user_preferences WHERE key = ?', (key,))
            result = cursor.fetchone()
            return result[0] if result else None
    
    def store_pattern(self, pattern_type: str, pattern_data: Dict, confidence: float = 0.5):
        """Store a learned pattern."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO learned_patterns 
                (pattern_type, pattern_data, confidence)
                VALUES (?, ?, ?)
            ''', (pattern_type, json.dumps(pattern_data), confidence))
            conn.commit()
    
    def get_patterns(self, pattern_type: str = None) -> List[Dict]:
        """Retrieve learned patterns."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if pattern_type:
                cursor.execute('''
                    SELECT * FROM learned_patterns 
                    WHERE pattern_type = ? 
                    ORDER BY confidence DESC, usage_count DESC
                ''', (pattern_type,))
            else:
                cursor.execute('''
                    SELECT * FROM learned_patterns 
                    ORDER BY confidence DESC, usage_count DESC
                ''')
            
            columns = [desc[0] for desc in cursor.description]
            patterns = []
            for row in cursor.fetchall():
                pattern = dict(zip(columns, row))
                pattern['pattern_data'] = json.loads(pattern['pattern_data'])
                patterns.append(pattern)
            
            return patterns
    
    def store_location_preference(self, context: str, path: str):
        """Store a location preference for a specific context."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if preference already exists
            cursor.execute('''
                SELECT id, usage_count FROM location_preferences 
                WHERE context = ? AND preferred_path = ?
            ''', (context, path))
            result = cursor.fetchone()
            
            if result:
                # Update existing preference
                cursor.execute('''
                    UPDATE location_preferences 
                    SET usage_count = usage_count + 1, last_used = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (result[0],))
            else:
                # Create new preference
                cursor.execute('''
                    INSERT INTO location_preferences (context, preferred_path)
                    VALUES (?, ?)
                ''', (context, path))
            
            conn.commit()
    
    def get_preferred_location(self, context: str) -> Optional[str]:
        """Get the most preferred location for a context."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT preferred_path FROM location_preferences 
                WHERE context = ? 
                ORDER BY usage_count DESC, last_used DESC 
                LIMIT 1
            ''', (context,))
            result = cursor.fetchone()
            return result[0] if result else None


# Global memory instance
_atom_memory = AtomMemory()


# ============================================================================
# LEARNING AND MEMORY TOOLS
# ============================================================================

@tool
def remember_preference(key: str, value: str, category: str = "general"):
    """
    Remember a user preference or setting.
    
    Args:
        key: Preference key (e.g., "default_save_location", "email_signature")
        value: Preference value
        category: Category for organization (e.g., "files", "email", "calendar")
        
    Returns:
        Confirmation message
    """
    try:
        _atom_memory.store_preference(key, value, category)
        return f"✅ Remembered: {key} = {value} (category: {category})"
    except Exception as e:
        return f"❌ Error storing preference: {str(e)}"

@tool
def recall_preference(key: str):
    """
    Recall a previously stored user preference.
    
    Args:
        key: Preference key to recall
        
    Returns:
        Stored preference value or not found message
    """
    try:
        value = _atom_memory.get_preference(key)
        if value:
            return f"📋 {key}: {value}"
        else:
            return f"🔍 No preference found for '{key}'"
    except Exception as e:
        return f"❌ Error retrieving preference: {str(e)}"

@tool
def learn_location_preference(context: str, path: str):
    """
    Learn user's preferred location for specific contexts.
    
    Args:
        context: Context description (e.g., "save_reports", "backup_files", "screenshots")
        path: Preferred file path for this context
        
    Returns:
        Learning confirmation
    """
    try:
        _atom_memory.store_location_preference(context, path)
        return f"🧠 Learned: For '{context}', you prefer using '{path}'"
    except Exception as e:
        return f"❌ Error learning location preference: {str(e)}"

@tool
def suggest_location(context: str):
    """
    Suggest a file location based on learned user preferences.
    
    Args:
        context: Context for the suggestion (e.g., "save_reports", "backup_files")
        
    Returns:
        Suggested location or default suggestion
    """
    try:
        preferred = _atom_memory.get_preferred_location(context)
        if preferred:
            return f"💡 Suggestion: Based on your patterns, try '{preferred}' for '{context}'"
        else:
            return f"🤔 No learned preference for '{context}' yet. I'll remember your choice for next time."
    except Exception as e:
        return f"❌ Error getting location suggestion: {str(e)}"

@tool
def get_command_patterns(days: int = 30):
    """
    Analyze command usage patterns from recent history.
    
    Args:
        days: Number of days to analyze (default: 30)
        
    Returns:
        Analysis of command patterns and frequent tasks
    """
    try:
        history = _atom_memory.get_command_history(limit=1000)
        
        if not history:
            return "📊 No command history available yet."
        
        # Analyze patterns
        command_types = Counter()
        frequent_commands = Counter()
        recent_cutoff = datetime.now() - timedelta(days=days)
        
        for entry in history:
            timestamp = datetime.fromisoformat(entry['timestamp'])
            if timestamp >= recent_cutoff:
                command_types[entry['command_type']] += 1
                # Extract command keywords for pattern analysis
                words = entry['command'].lower().split()[:3]  # First 3 words
                command_pattern = ' '.join(words)
                frequent_commands[command_pattern] += 1
        
        # Generate report
        report = f"📊 Command Patterns (Last {days} days):\\n\\n"
        
        # Most used command types
        report += "🔥 Most Used Categories:\\n"
        for cmd_type, count in command_types.most_common(5):
            report += f"  • {cmd_type}: {count} times\\n"
        
        report += "\\n🔄 Frequent Command Patterns:\\n"
        for pattern, count in frequent_commands.most_common(8):
            if count > 1:  # Only show patterns used more than once
                report += f"  • '{pattern}': {count} times\\n"
        
        return report
        
    except Exception as e:
        return f"❌ Error analyzing patterns: {str(e)}"

@tool
def get_recent_activity(hours: int = 24):
    """
    Get recent activity summary.
    
    Args:
        hours: Number of hours to look back (default: 24)
        
    Returns:
        Summary of recent commands and activities
    """
    try:
        cutoff = datetime.now() - timedelta(hours=hours)
        history = _atom_memory.get_command_history(limit=50)
        
        recent = [entry for entry in history 
                 if datetime.fromisoformat(entry['timestamp']) >= cutoff]
        
        if not recent:
            return f"📝 No activity in the last {hours} hours."
        
        summary = f"📈 Activity Summary (Last {hours} hours):\\n"
        summary += f"Total commands: {len(recent)}\\n\\n"
        
        # Show recent commands
        summary += "🕐 Recent Commands:\\n"
        for entry in recent[:10]:  # Show last 10
            time_str = datetime.fromisoformat(entry['timestamp']).strftime("%H:%M")
            success_icon = "✅" if entry['success'] else "❌"
            summary += f"  {time_str} {success_icon} {entry['command'][:50]}{'...' if len(entry['command']) > 50 else ''}\\n"
        
        return summary
        
    except Exception as e:
        return f"❌ Error getting recent activity: {str(e)}"

@tool
def store_context_information(info_type: str, information: str):
    """
    Store contextual information for future reference.
    
    Args:
        info_type: Type of information (e.g., "project_info", "meeting_notes", "task_context")
        information: The information to store
        
    Returns:
        Confirmation of storage
    """
    try:
        # Store as a pattern for easy retrieval
        pattern_data = {
            "info_type": info_type,
            "information": information,
            "stored_at": datetime.now().isoformat()
        }
        
        _atom_memory.store_pattern("context_info", pattern_data, confidence=0.8)
        return f"💾 Stored {info_type}: {information[:100]}{'...' if len(information) > 100 else ''}"
        
    except Exception as e:
        return f"❌ Error storing context: {str(e)}"

@tool
def retrieve_context_information(info_type: str = None):
    """
    Retrieve stored contextual information.
    
    Args:
        info_type: Optional filter by information type
        
    Returns:
        Retrieved contextual information
    """
    try:
        patterns = _atom_memory.get_patterns("context_info")
        
        if info_type:
            patterns = [p for p in patterns 
                       if p['pattern_data'].get('info_type') == info_type]
        
        if not patterns:
            return f"🔍 No context information found" + (f" for type '{info_type}'" if info_type else "")
        
        result = "📚 Stored Context Information:\\n\\n"
        for pattern in patterns[:10]:  # Limit to 10 most relevant
            data = pattern['pattern_data']
            stored_time = datetime.fromisoformat(data['stored_at']).strftime("%Y-%m-%d %H:%M")
            result += f"📝 {data['info_type']} ({stored_time}):\\n"
            result += f"   {data['information']}\\n\\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error retrieving context: {str(e)}"


def record_command_execution(command: str, command_type: str, result: str, 
                           success: bool, execution_time: float = 0.0):
    """Helper function to record command executions."""
    try:
        _atom_memory.store_command(command, command_type, result, success, execution_time)
    except Exception:
        pass  # Silent fail to not interrupt main operations