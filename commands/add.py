import os
import sys
import hashlib
import zlib
from .gitignore import GitIgnore
from indexfile import add_file_to_index

def add():
    if len(sys.argv) < 3:
        print("Usage: githetic add <file>...")
        return
    
    current_dir = os.getcwd()
    git_dir = os.path.join(current_dir, '.githetic')
    
    if not os.path.exists(git_dir):
        print("Error: Not a githetic repository. Run 'githetic init' first.")
        return
    
    objects_dir = os.path.join(git_dir, 'objects')
    
    files_to_add = sys.argv[2:]
    expanded_files = []
    
    for pattern in files_to_add:
        if pattern == '*':
            for root, dirs, files in os.walk('.'):
                if '.githetic' in dirs:
                    dirs.remove('.githetic')
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path.startswith('./'):
                        file_path = file_path[2:]
                    expanded_files.append(file_path)
        elif '*' in pattern or '?' in pattern:
            import glob
            matched_files = glob.glob(pattern)
            expanded_files.extend(matched_files)
        else:
            expanded_files.append(pattern)
    
    gitignore = GitIgnore(current_dir)

    for file_path in expanded_files:
        if not os.path.exists(file_path):
            print(f"Error: '{file_path}' does not exist")
            continue

        if os.path.isdir(file_path):
            continue

        if gitignore.is_ignored(os.path.abspath(file_path)):
            print(f"Ignored '{file_path}' (matched .gitignore)")
            continue

        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Add blob header as Git does: "blob <size>\0<content>"
            header = f"blob {len(content)}\0".encode()
            store = header + content
            content_hash = hashlib.sha1(store).hexdigest()
            object_path = os.path.join(objects_dir, content_hash[:2], content_hash[2:])
            
            os.makedirs(os.path.dirname(object_path), exist_ok=True)

            if not os.path.exists(object_path):  
                compressed_content = zlib.compress(store)
                with open(object_path, 'wb') as f:
                    f.write(compressed_content)
            
            # Ajoute le fichier et son hash dans l'index texte
            add_file_to_index(file_path, content_hash)
            
            print(f"Added '{file_path}' to staging area")
            
        except Exception as e:
            print(f"Error adding '{file_path}': {e}")

if __name__ == "__main__":
    add()
