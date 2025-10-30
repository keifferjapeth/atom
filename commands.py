import subprocess
import re
import os
import shutil
import pathlib
import mimetypes
from datetime import datetime
from typing import List, Dict, Any

from langchain.agents import tool

@tool
def computer_applescript_action(apple_script):
    """
    Use this when you want to execute a command on the computer. The command should be in AppleScript.

    Always start with starting the app and activating it.

    If it's a calculation, use the calculator app.

    Use delay 0.5 between keystrokes.

    When possible click buttons instead of typing.

    Here are some examples of good AppleScript commands:

    Command: Create a new page in Notion
    AppleScript: tell application "Notion"
        activate
        delay 0.5
        tell application "System Events" to keystroke "n" using {{command down}}
    end tell

    Command: Search for a table nearby
    AppleScript: tell application "Google Chrome"
        activate
        delay 0.5
        open location "https://www.google.com/search?q=Table+nearby"
    end tell

    The AppleScript should be valid including quotations.

    Write the AppleScript for the Command:
    Command: 
    """
    print("Running\n", apple_script)

    return run_applescript(apple_script)

@tool
def chrome_get_the_links_on_the_page(input):
    """
    Use this when you want to get the links on the current page.

    You should use this before clicking on anything
    """
    return run_javascript('Array.from(document.querySelectorAll("a")).map(x => x.innerText + ": " + x.href).join(" - ")')[:4000]

@tool
def chrome_click_on_link(link):
    """
    Use this when you want to go to a link. 
    
    The link should be a url from a previous observation
    """
    return run_javascript(f'window.location.href = "{link}"')[:4000]

@tool
def chrome_read_the_page(input):
    """
    Use this when you want to read the page.
    """

    return run_javascript('document.body.innerText')[:4000]


# @tool
# def chrome_javascript_action(javascript):
#     """
#     Use this when you want to execute a javascript command on Chrome either to get data or trigger an action. The command should be in Javascript.

#     Here are some examples of good Javascript commands:

#     Command: Get the links on the page
#     document.querySelectorAll('a')

#     Command: Get the buttons on the page
#     document.querySelectorAll('button')

#     Command: Click the first button on the page
#     document.querySelectorAll('button')[0].click()

#     Write the Javascript for the command:
#     """

#     stdout = run_javascript(javascript)

#     return f"""
#     Current URL: {run_javascript('window.location.href')}

#     Result: {stdout}
#     """

@tool
def chrome_open_url(url):
    """
    Use this tool to open a URL in Chrome. It is recommended to use this tool before doing any other actions on Chrome.
    
    The URL should be a string. For example: https://gmail.com
    """
    script = f'''
    tell application "Google Chrome"
        open location "{url}"
    end tell
    '''

    return run_applescript(script)

def run_javascript(javascript):
    javascript = javascript.replace('"', '\\"')

    if javascript.startswith('open '):
        return "Invalid command, not javascript"

    script = f'''
    tell application "Google Chrome"
        tell active tab of front window
            execute javascript "{javascript}"
        end tell
    end tell
    '''
    
    return run_applescript(script)

def run_applescript(applescript):
    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = p.communicate(applescript.encode('utf-8'))

    if p.returncode != 0:
        raise Exception(stderr)

    decoded_text = stdout.decode("utf-8")

    return decoded_text


def say_text(text):
    run_applescript(f'say "{text}"')


# ============================================================================
# FILE MANAGEMENT TOOLS
# ============================================================================

@tool
def list_directory(path: str = "."):
    """
    List files and directories in the specified path.
    
    Args:
        path: Directory path to list (default: current directory)
        
    Returns:
        String with formatted list of files and directories
    """
    try:
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return f"Error: Path '{path}' does not exist"
        
        if not os.path.isdir(path):
            return f"Error: '{path}' is not a directory"
        
        items = []
        for item in sorted(os.listdir(path)):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                items.append(f"📁 {item}/")
            else:
                size = os.path.getsize(item_path)
                size_str = format_file_size(size)
                items.append(f"📄 {item} ({size_str})")
        
        return f"Contents of '{path}':\n" + "\n".join(items)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@tool
def create_directory(path: str):
    """
    Create a new directory at the specified path.
    
    Args:
        path: Path where to create the directory
        
    Returns:
        Success or error message
    """
    try:
        path = os.path.expanduser(path)
        os.makedirs(path, exist_ok=True)
        return f"Successfully created directory: {path}"
    except Exception as e:
        return f"Error creating directory: {str(e)}"

@tool
def copy_file(source: str, destination: str):
    """
    Copy a file from source to destination.
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        Success or error message
    """
    try:
        source = os.path.expanduser(source)
        destination = os.path.expanduser(destination)
        
        if not os.path.exists(source):
            return f"Error: Source file '{source}' does not exist"
        
        if os.path.isfile(source):
            shutil.copy2(source, destination)
            return f"Successfully copied '{source}' to '{destination}'"
        else:
            return f"Error: '{source}' is not a file"
    except Exception as e:
        return f"Error copying file: {str(e)}"

@tool
def move_file(source: str, destination: str):
    """
    Move or rename a file from source to destination.
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        Success or error message
    """
    try:
        source = os.path.expanduser(source)
        destination = os.path.expanduser(destination)
        
        if not os.path.exists(source):
            return f"Error: Source '{source}' does not exist"
        
        shutil.move(source, destination)
        return f"Successfully moved '{source}' to '{destination}'"
    except Exception as e:
        return f"Error moving file: {str(e)}"

@tool
def delete_file(path: str):
    """
    Delete a file or directory at the specified path.
    
    Args:
        path: Path to the file or directory to delete
        
    Returns:
        Success or error message
    """
    try:
        path = os.path.expanduser(path)
        
        if not os.path.exists(path):
            return f"Error: Path '{path}' does not exist"
        
        if os.path.isfile(path):
            os.remove(path)
            return f"Successfully deleted file: {path}"
        elif os.path.isdir(path):
            shutil.rmtree(path)
            return f"Successfully deleted directory: {path}"
    except Exception as e:
        return f"Error deleting: {str(e)}"

@tool
def get_file_info(path: str):
    """
    Get detailed information about a file or directory.
    
    Args:
        path: Path to the file or directory
        
    Returns:
        Detailed file information
    """
    try:
        path = os.path.expanduser(path)
        
        if not os.path.exists(path):
            return f"Error: Path '{path}' does not exist"
        
        stat = os.stat(path)
        mime_type, _ = mimetypes.guess_type(path)
        
        info = {
            "path": path,
            "name": os.path.basename(path),
            "type": "directory" if os.path.isdir(path) else "file",
            "size": format_file_size(stat.st_size),
            "size_bytes": stat.st_size,
            "mime_type": mime_type or "unknown",
            "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "permissions": oct(stat.st_mode)[-3:],
        }
        
        result = f"File Information for '{path}':\n"
        for key, value in info.items():
            result += f"  {key.capitalize()}: {value}\n"
        
        return result
    except Exception as e:
        return f"Error getting file info: {str(e)}"

@tool
def read_file_content(path: str, lines: int = None):
    """
    Read and return the content of a text file.
    
    Args:
        path: Path to the text file
        lines: Optional number of lines to read from the beginning
        
    Returns:
        File content or error message
    """
    try:
        path = os.path.expanduser(path)
        
        if not os.path.exists(path):
            return f"Error: File '{path}' does not exist"
        
        if not os.path.isfile(path):
            return f"Error: '{path}' is not a file"
        
        with open(path, 'r', encoding='utf-8') as f:
            if lines:
                content = ''.join(f.readline() for _ in range(lines))
            else:
                content = f.read()
        
        # Limit output to prevent overwhelming the agent
        if len(content) > 2000:
            content = content[:2000] + "\n... (content truncated)"
        
        return f"Content of '{path}':\n{content}"
    except UnicodeDecodeError:
        return f"Error: '{path}' appears to be a binary file"
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool
def search_files(directory: str, pattern: str, content_search: bool = False):
    """
    Search for files by name pattern or content.
    
    Args:
        directory: Directory to search in
        pattern: Search pattern (filename pattern or text to search in files)
        content_search: If True, search inside file contents; if False, search filenames
        
    Returns:
        List of matching files
    """
    try:
        directory = os.path.expanduser(directory)
        
        if not os.path.exists(directory):
            return f"Error: Directory '{directory}' does not exist"
        
        matches = []
        
        if content_search:
            # Search file contents
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if pattern.lower() in content.lower():
                                matches.append(file_path)
                    except (UnicodeDecodeError, PermissionError):
                        continue  # Skip binary files or files without permission
        else:
            # Search filenames
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if pattern.lower() in file.lower():
                        matches.append(os.path.join(root, file))
        
        if matches:
            result = f"Found {len(matches)} matches for '{pattern}':\n"
            for match in matches[:20]:  # Limit to first 20 results
                result += f"  {match}\n"
            if len(matches) > 20:
                result += f"  ... and {len(matches) - 20} more matches"
            return result
        else:
            return f"No matches found for '{pattern}'"
            
    except Exception as e:
        return f"Error searching files: {str(e)}"

# ============================================================================
# TERMINAL EXECUTION TOOLS
# ============================================================================

@tool
def run_terminal_command(command: str, working_directory: str = None):
    """
    Execute a terminal command and return the output.
    
    Args:
        command: Shell command to execute
        working_directory: Optional working directory for the command
        
    Returns:
        Command output or error message
    """
    try:
        if working_directory:
            working_directory = os.path.expanduser(working_directory)
            if not os.path.exists(working_directory):
                return f"Error: Working directory '{working_directory}' does not exist"
        
        # Security: Basic command filtering to prevent dangerous operations
        dangerous_patterns = ['rm -rf /', 'sudo rm', 'format', 'mkfs', '> /dev/']
        for pattern in dangerous_patterns:
            if pattern in command.lower():
                return f"Error: Command rejected for security reasons"
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=30  # 30 second timeout
        )
        
        output = ""
        if result.stdout:
            output += f"Output:\n{result.stdout}\n"
        if result.stderr:
            output += f"Errors:\n{result.stderr}\n"
        
        output += f"Return code: {result.returncode}"
        
        # Limit output length
        if len(output) > 2000:
            output = output[:2000] + "\n... (output truncated)"
        
        return output
        
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except Exception as e:
        return f"Error executing command: {str(e)}"

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
