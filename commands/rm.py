import os
import sys
from indexfile import remove_file_from_index

def rm():
    """Remove files from working directory and index"""
    if len(sys.argv) < 3:
        print("Usage: githetic rm <file>...")
        return

    files_to_remove = sys.argv[2:]

    current_dir = os.getcwd()
    git_dir = os.path.join(current_dir, '.githetic')

    if not os.path.exists(git_dir):
        print("Error: Not a githetic repository. Run 'githetic init' first.")
        return

    # Remove files from the index first
    for filepath in files_to_remove:
        remove_file_from_index(filepath)

    index_file = os.path.join(git_dir, 'index')
    index_entries = []
    if os.path.exists(index_file):
        with open(index_file, 'r') as f:
            index_entries = f.readlines()

    new_index_entries = []
    removed_from_index = set()

    for entry in index_entries:
        entry = entry.strip()
        if not entry:
            continue
        
        parts = entry.split(' ', 1)
        if len(parts) != 2:
            continue
        
        hash_value, file_path = parts

        if file_path in files_to_remove and file_path not in removed_from_index:
            # Try to remove the file from the working directory
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Removed '{file_path}' from working directory")
                except Exception as e:
                    print(f"Error removing '{file_path}' from working directory: {e}")
            else:
                print(f"Warning: '{file_path}' not found in working directory")

            print(f"Removed '{file_path}' from index")
            removed_from_index.add(file_path)
        else:
            new_index_entries.append(entry)

    # Rewrite the index file without the removed files
    with open(index_file, 'w') as f:
        for entry in new_index_entries:
            f.write(entry + '\n')

    # In case some files are not in the index but exist in working dir, remove them
    for filepath in files_to_remove:
        if os.path.exists(filepath) and filepath not in removed_from_index:
            try:
                os.remove(filepath)
                print(f"Removed '{filepath}' from working directory")
            except Exception as e:
                print(f"Error removing '{filepath}' from working directory: {e}")

if __name__ == "__main__":
    rm()
