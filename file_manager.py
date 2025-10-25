import os
import shutil
import json # NEW: Added for JSON file handling

def create_text_file(file_name, content=""):
    """
    Creates a new text file with the specified name and optional content.
    Returns a success message or an error message.
    """
    try:
        # Sanitize the file name to prevent directory traversal attacks
        safe_file_name = os.path.basename(file_name)
        with open(safe_file_name, "w") as f:
            f.write(content)
        return f"File '{safe_file_name}' created successfully."
    except Exception as e:
        return f"An error occurred while creating the file: {e}"

def read_text_file(file_name):
    """
    Reads the content of a text file and returns it as a string.
    Returns the file content or an error message.
    """
    try:
        with open(file_name, "r") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Error: The file '{file_name}' was not found."
    except Exception as e:
        return f"An error occurred while reading the file: {e}"

def list_directory(path="."):
    """
    Lists all files and directories in the specified path.
    Returns a formatted string of contents or an error message.
    """
    try:
        contents = os.listdir(path)
        if not contents:
            return "The directory is empty."
        
        file_list = "\n".join(contents)
        return f"Here are the contents of the directory:\n{file_list}"
    except FileNotFoundError:
        return f"Error: The directory '{path}' was not found."
    except Exception as e:
        return f"An error occurred while listing the directory: {e}"

def delete_file(file_name):
    """
    Deletes a file with the specified name.
    Returns a success message or an error message.
    """
    try:
        os.remove(file_name)
        return f"File '{file_name}' deleted successfully."
    except FileNotFoundError:
        return f"Error: The file '{file_name}' was not found."
    except Exception as e:
        return f"An error occurred while deleting the file: {e}"

def delete_folder(folder_name):
    """
    Deletes a folder and all its contents.
    Returns a success message or an error message.
    """
    try:
        shutil.rmtree(folder_name)
        return f"Folder '{folder_name}' and all its contents deleted successfully."
    except FileNotFoundError:
        return f"Error: The folder '{folder_name}' was not found."
    except Exception as e:
        return f"An error occurred while deleting the folder: {e}"

# --- NEW FUNCTIONS FOR DATA DELETION ---

def clear_json_file(file_path, default_content={}):
    """
    Clears the content of a JSON file by overwriting it with empty content.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(default_content, f, indent=4)
        print(f"Successfully cleared data in: {file_path}")
        return True
    except Exception as e:
        print(f"Warning: Could not clear JSON file {file_path}. Error: {e}")
        return False

def delete_all_user_data():
    """
    Handles the command to clear or delete all personal data files.
    """
    # Files to clear (overwritten with empty content/default structure)
    # This prevents the program from crashing on startup due to missing files
    files_to_clear = [
        ('knowledge_base.json', {}), # Empty dictionary for KB
        ('contacts.json', {}),       # Empty dictionary for contacts
        ('phrasings.json', {}),      # Empty dictionary for synonyms
        # Reset user data to initial structure
        ('user_data.json', {"name": "User", "honorific": "Sir", "default_city": "City", "details": {}}) 
    ]
    
    # Files to delete (removed entirely)
    files_to_delete = [
        'email_creds.txt', # Assume this is where credentials might be stored
    ]
    
    success_count = 0
    total_files = len(files_to_clear) + len(files_to_delete)
    
    # Clear JSON files
    for file_path, default_content in files_to_clear:
        if clear_json_file(file_path, default_content):
            success_count += 1
            
    # Delete other files
    for file_path in files_to_delete:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Successfully deleted file: {file_path}")
            else:
                print(f"File not found (Skipped): {file_path}")
            success_count += 1
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    if success_count == total_files:
        return "All saved knowledge, contacts, and personal data files have been successfully cleared and reset."
    elif success_count > 0:
         return f"Some personal data was cleared, but {total_files - success_count} files could not be processed. Please check the console."
    else:
        return "An error occurred while trying to delete any data. Please check the console for details."