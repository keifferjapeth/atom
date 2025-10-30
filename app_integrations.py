"""
Advanced macOS Application Integration for Atom AI Assistant.
Provides comprehensive control and integration with native macOS apps.
"""

import subprocess
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from langchain.agents import tool


# ============================================================================
# FINDER & FILE SYSTEM INTEGRATION
# ============================================================================

@tool
def finder_open_location(path: str):
    """
    Open a specific location in Finder.
    
    Args:
        path: Path to open in Finder
        
    Returns:
        Success message or error
    """
    try:
        path = os.path.expanduser(path)
        script = f'''
        tell application "Finder"
            activate
            open POSIX file "{path}"
        end tell
        '''
        return run_applescript(script)
    except Exception as e:
        return f"Error opening Finder: {str(e)}"

@tool
def finder_get_selection():
    """
    Get currently selected items in Finder.
    
    Returns:
        List of selected file paths
    """
    try:
        script = '''
        tell application "Finder"
            set selectedItems to selection
            set itemPaths to {}
            repeat with anItem in selectedItems
                set end of itemPaths to POSIX path of (anItem as alias)
            end repeat
            return itemPaths
        end tell
        '''
        result = run_applescript(script)
        return f"Selected items in Finder: {result}"
    except Exception as e:
        return f"Error getting Finder selection: {str(e)}"

@tool
def finder_create_folder(parent_path: str, folder_name: str):
    """
    Create a new folder in Finder at the specified location.
    
    Args:
        parent_path: Parent directory path
        folder_name: Name of new folder
        
    Returns:
        Success message or error
    """
    try:
        parent_path = os.path.expanduser(parent_path)
        script = f'''
        tell application "Finder"
            activate
            set targetFolder to POSIX file "{parent_path}" as alias
            make new folder at targetFolder with properties {{name:"{folder_name}"}}
        end tell
        '''
        run_applescript(script)
        return f"Successfully created folder '{folder_name}' in '{parent_path}'"
    except Exception as e:
        return f"Error creating folder: {str(e)}"


# ============================================================================
# MAIL INTEGRATION
# ============================================================================

@tool
def mail_compose_email(to: str, subject: str = "", body: str = ""):
    """
    Compose a new email in Mail app.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content
        
    Returns:
        Success message or error
    """
    try:
        script = f'''
        tell application "Mail"
            activate
            set newMessage to make new outgoing message with properties {{subject:"{subject}", content:"{body}"}}
            tell newMessage
                make new to recipient at end of to recipients with properties {{address:"{to}"}}
            end tell
            set visible of newMessage to true
        end tell
        '''
        run_applescript(script)
        return f"Composed email to {to} with subject: '{subject}'"
    except Exception as e:
        return f"Error composing email: {str(e)}"

@tool
def mail_get_unread_count():
    """
    Get the count of unread emails in Mail.
    
    Returns:
        Number of unread emails
    """
    try:
        script = '''
        tell application "Mail"
            set unreadCount to unread count of inbox
            return unreadCount
        end tell
        '''
        result = run_applescript(script)
        return f"Unread emails: {result.strip()}"
    except Exception as e:
        return f"Error checking unread emails: {str(e)}"

@tool
def mail_get_recent_emails(count: int = 5):
    """
    Get recent emails from Mail inbox.
    
    Args:
        count: Number of recent emails to retrieve
        
    Returns:
        List of recent email subjects and senders
    """
    try:
        script = f'''
        tell application "Mail"
            set recentMessages to messages 1 thru {count} of inbox
            set emailInfo to {{}}
            repeat with aMessage in recentMessages
                set messageInfo to (subject of aMessage) & " - From: " & (sender of aMessage)
                set end of emailInfo to messageInfo
            end repeat
            return emailInfo
        end tell
        '''
        result = run_applescript(script)
        return f"Recent emails:\\n{result}"
    except Exception as e:
        return f"Error getting recent emails: {str(e)}"


# ============================================================================
# CALENDAR INTEGRATION
# ============================================================================

@tool
def calendar_create_event(title: str, start_date: str, end_date: str = None, notes: str = ""):
    """
    Create a new calendar event.
    
    Args:
        title: Event title
        start_date: Start date/time (e.g., "2024-01-15 14:30")
        end_date: End date/time (optional, defaults to 1 hour after start)
        notes: Event notes
        
    Returns:
        Success message or error
    """
    try:
        if not end_date:
            # Default to 1 hour after start
            from datetime import datetime, timedelta
            start_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
            end_dt = start_dt + timedelta(hours=1)
            end_date = end_dt.strftime("%Y-%m-%d %H:%M")
        
        script = f'''
        tell application "Calendar"
            activate
            tell calendar "Calendar"
                make new event with properties {{summary:"{title}", start date:date "{start_date}", end date:date "{end_date}", description:"{notes}"}}
            end tell
        end tell
        '''
        run_applescript(script)
        return f"Created calendar event: '{title}' on {start_date}"
    except Exception as e:
        return f"Error creating calendar event: {str(e)}"

@tool
def calendar_get_todays_events():
    """
    Get today's calendar events.
    
    Returns:
        List of today's events
    """
    try:
        script = '''
        tell application "Calendar"
            set todayStart to current date
            set hours of todayStart to 0
            set minutes of todayStart to 0
            set seconds of todayStart to 0
            
            set todayEnd to todayStart + (24 * hours)
            
            set todaysEvents to {}
            repeat with aCalendar in calendars
                set eventsInCalendar to (every event of aCalendar whose start date ≥ todayStart and start date < todayEnd)
                repeat with anEvent in eventsInCalendar
                    set eventInfo to (summary of anEvent) & " at " & (start date of anEvent as string)
                    set end of todaysEvents to eventInfo
                end repeat
            end repeat
            return todaysEvents
        end tell
        '''
        result = run_applescript(script)
        return f"Today's events:\\n{result}"
    except Exception as e:
        return f"Error getting today's events: {str(e)}"


# ============================================================================
# NOTES INTEGRATION
# ============================================================================

@tool
def notes_create_note(title: str, content: str, folder: str = "Notes"):
    """
    Create a new note in the Notes app.
    
    Args:
        title: Note title
        content: Note content
        folder: Folder to create note in (default: "Notes")
        
    Returns:
        Success message or error
    """
    try:
        script = f'''
        tell application "Notes"
            activate
            tell folder "{folder}"
                make new note with properties {{name:"{title}", body:"{content}"}}
            end tell
        end tell
        '''
        run_applescript(script)
        return f"Created note '{title}' in folder '{folder}'"
    except Exception as e:
        return f"Error creating note: {str(e)}"

@tool
def notes_search_notes(query: str):
    """
    Search for notes containing specific text.
    
    Args:
        query: Text to search for in notes
        
    Returns:
        List of matching notes
    """
    try:
        script = f'''
        tell application "Notes"
            set matchingNotes to {{}}
            repeat with aNote in notes
                if (body of aNote contains "{query}") then
                    set noteInfo to (name of aNote) & ": " & (body of aNote)
                    set end of matchingNotes to noteInfo
                end if
            end repeat
            return matchingNotes
        end tell
        '''
        result = run_applescript(script)
        return f"Notes matching '{query}':\\n{result}"
    except Exception as e:
        return f"Error searching notes: {str(e)}"


# ============================================================================
# SYSTEM UTILITIES
# ============================================================================

@tool
def system_take_screenshot(filename: str = None, area: str = "screen"):
    """
    Take a screenshot using macOS built-in tools.
    
    Args:
        filename: Optional filename (defaults to timestamp)
        area: "screen" for full screen, "window" for active window, "selection" for user selection
        
    Returns:
        Success message with screenshot location
    """
    try:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        desktop_path = os.path.expanduser("~/Desktop")
        full_path = os.path.join(desktop_path, filename)
        
        if area == "screen":
            cmd = ["screencapture", "-x", full_path]
        elif area == "window":
            cmd = ["screencapture", "-w", full_path]
        elif area == "selection":
            cmd = ["screencapture", "-s", full_path]
        else:
            return f"Error: Invalid area '{area}'. Use 'screen', 'window', or 'selection'"
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return f"Screenshot saved to: {full_path}"
        else:
            return f"Error taking screenshot: {result.stderr}"
            
    except Exception as e:
        return f"Error taking screenshot: {str(e)}"

@tool
def system_get_app_list():
    """
    Get list of installed applications.
    
    Returns:
        List of installed applications
    """
    try:
        script = '''
        tell application "System Events"
            set appList to name of every application process
            return appList
        end tell
        '''
        result = run_applescript(script)
        return f"Running applications:\\n{result}"
    except Exception as e:
        return f"Error getting app list: {str(e)}"

@tool
def system_open_app(app_name: str):
    """
    Open a macOS application by name.
    
    Args:
        app_name: Name of the application to open
        
    Returns:
        Success message or error
    """
    try:
        script = f'''
        tell application "{app_name}"
            activate
        end tell
        '''
        run_applescript(script)
        return f"Opened application: {app_name}"
    except Exception as e:
        return f"Error opening {app_name}: {str(e)}"

@tool
def system_quit_app(app_name: str):
    """
    Quit a macOS application by name.
    
    Args:
        app_name: Name of the application to quit
        
    Returns:
        Success message or error
    """
    try:
        script = f'''
        tell application "{app_name}"
            quit
        end tell
        '''
        run_applescript(script)
        return f"Quit application: {app_name}"
    except Exception as e:
        return f"Error quitting {app_name}: {str(e)}"


# ============================================================================
# REMINDERS INTEGRATION
# ============================================================================

@tool
def reminders_create_reminder(title: str, due_date: str = None, notes: str = "", list_name: str = "Reminders"):
    """
    Create a new reminder in the Reminders app.
    
    Args:
        title: Reminder title
        due_date: Due date (e.g., "2024-01-15 14:30")
        notes: Reminder notes
        list_name: Reminders list name
        
    Returns:
        Success message or error
    """
    try:
        due_date_part = f', due date:date "{due_date}"' if due_date else ""
        
        script = f'''
        tell application "Reminders"
            tell list "{list_name}"
                make new reminder with properties {{name:"{title}", body:"{notes}"{due_date_part}}}
            end tell
        end tell
        '''
        run_applescript(script)
        return f"Created reminder: '{title}' in list '{list_name}'"
    except Exception as e:
        return f"Error creating reminder: {str(e)}"

@tool
def reminders_get_list():
    """
    Get current reminders from the Reminders app.
    
    Returns:
        List of current reminders
    """
    try:
        script = '''
        tell application "Reminders"
            set allReminders to {}
            repeat with aList in lists
                repeat with aReminder in reminders of aList
                    if not completed of aReminder then
                        set reminderInfo to (name of aReminder) & " in " & (name of aList)
                        set end of allReminders to reminderInfo
                    end if
                end repeat
            end repeat
            return allReminders
        end tell
        '''
        result = run_applescript(script)
        return f"Current reminders:\\n{result}"
    except Exception as e:
        return f"Error getting reminders: {str(e)}"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def run_applescript(script: str) -> str:
    """Execute AppleScript and return the result."""
    try:
        process = subprocess.Popen(
            ['osascript', '-'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(script)
        
        if process.returncode != 0:
            raise Exception(f"AppleScript error: {stderr}")
        
        return stdout.strip()
        
    except Exception as e:
        raise Exception(f"Failed to execute AppleScript: {str(e)}")