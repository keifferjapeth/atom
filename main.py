import sys
import os

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

from commands import (
    # Browser automation
    chrome_click_on_link, chrome_get_the_links_on_the_page, chrome_open_url, chrome_read_the_page,
    # Computer automation
    computer_applescript_action, say_text,
    # File management
    list_directory, create_directory, copy_file, move_file, delete_file, 
    get_file_info, read_file_content, search_files,
    # Terminal execution
    run_terminal_command
)

# Import new Atom capabilities
try:
    from app_integrations import (
        # Finder integration
        finder_open_location, finder_get_selection, finder_create_folder,
        # Mail integration
        mail_compose_email, mail_get_unread_count, mail_get_recent_emails,
        # Calendar integration
        calendar_create_event, calendar_get_todays_events,
        # Notes integration
        notes_create_note, notes_search_notes,
        # System utilities
        system_take_screenshot, system_get_app_list, system_open_app, system_quit_app,
        # Reminders integration
        reminders_create_reminder, reminders_get_list
    )
    APP_TOOLS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  App integration tools not available: {e}")
    APP_TOOLS_AVAILABLE = False

try:
    from learning_system import (
        remember_preference, recall_preference, learn_location_preference,
        suggest_location, get_command_patterns, get_recent_activity,
        store_context_information, retrieve_context_information,
        record_command_execution
    )
    LEARNING_TOOLS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Learning system not available: {e}")
    LEARNING_TOOLS_AVAILABLE = False

try:
    from data_analysis import (
        analyze_csv_file, csv_query, analyze_json_file, json_extract_keys,
        analyze_directory_structure, find_duplicate_files
    )
    DATA_ANALYSIS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Data analysis tools not available: {e}")
    DATA_ANALYSIS_AVAILABLE = False

from keychain_manager import get_openai_api_key_with_fallback

def main(command):
    # Get API key from Keychain with fallbacks
    api_key = get_openai_api_key_with_fallback()
    if not api_key:
        print("❌ No OpenAI API key available. Please set up your API key first.")
        return
    
    # Set the API key for OpenAI
    os.environ["OPENAI_API_KEY"] = api_key
    
    llm = OpenAI(temperature=0)

    tools = [
        # Core automation tools
        computer_applescript_action,
        chrome_open_url,
        chrome_get_the_links_on_the_page,
        chrome_click_on_link,
        chrome_read_the_page,
        
        # File management tools
        list_directory,
        create_directory,
        copy_file,
        move_file,
        delete_file,
        get_file_info,
        read_file_content,
        search_files,
        
        # Terminal execution
        run_terminal_command
    ]
    
    # Add macOS app integration tools if available
    if APP_TOOLS_AVAILABLE:
        tools.extend([
            # Finder tools
            finder_open_location,
            finder_get_selection,
            finder_create_folder,
            
            # Mail tools
            mail_compose_email,
            mail_get_unread_count,
            mail_get_recent_emails,
            
            # Calendar tools
            calendar_create_event,
            calendar_get_todays_events,
            
            # Notes tools
            notes_create_note,
            notes_search_notes,
            
            # System tools
            system_take_screenshot,
            system_get_app_list,
            system_open_app,
            system_quit_app,
            
            # Reminders tools
            reminders_create_reminder,
            reminders_get_list
        ])
        print("✅ Loaded macOS app integration tools")
    
    # Add learning and memory tools if available
    if LEARNING_TOOLS_AVAILABLE:
        tools.extend([
            remember_preference,
            recall_preference,
            learn_location_preference,
            suggest_location,
            get_command_patterns,
            get_recent_activity,
            store_context_information,
            retrieve_context_information
        ])
        print("🧠 Loaded learning and memory tools")
    
    # Add data analysis tools if available
    if DATA_ANALYSIS_AVAILABLE:
        tools.extend([
            analyze_csv_file,
            csv_query,
            analyze_json_file,
            json_extract_keys,
            analyze_directory_structure,
            find_duplicate_files
        ])
        print("📊 Loaded data analysis tools")

    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

    result = agent.run(command)

    if result:
        say_text(f'The result is {result}')
    else:
        say_text(f'Finished doing {command}')

if __name__ == "__main__":
    command = sys.argv[1]
    if not command:
        print("Please provide a command to execute e.g. python main.py 'Open the calculator app'")
        exit(1)

    main(command)
