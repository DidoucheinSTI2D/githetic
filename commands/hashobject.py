import os
import sys
import hashlib
import zlib

def hash_object(file_path, write=False):
    """Calculate the SHA-1 hash of a file's content and optionally write it to the object store
    
    Args:
        file_path (str): Path to the file to hash
        write (bool): Whether to write the object to the object store
        
    Returns:
        str: The SHA-1 hash of the file's content
    """
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
        
    # Calculate the SHA-1 hash of the content
    header = f"blob {len(content)}\0".encode()
    store = header + content
    sha1 = hashlib.sha1(store).hexdigest()
    
    if write:
        current_dir = os.getcwd()
        git_dir = find_git_dir(current_dir)
        if not git_dir:
            print("Error: Not a githetic repository (or any of the parent directories)")
            sys.exit(1)
            
    
        object_dir = os.path.join(git_dir, 'objects', sha1[:2])
        if not os.path.exists(object_dir):
            os.makedirs(object_dir)
            

        object_path = os.path.join(object_dir, sha1[2:])
        if not os.path.exists(object_path):
            compressed = zlib.compress(store)
            with open(object_path, 'wb') as f:
                f.write(compressed)
    
    return sha1

def find_git_dir(start_dir):
    """Find the .githetic directory by traversing up the directory tree
    
    Args:
        start_dir (str): Directory to start the search from
        
    Returns:
        str or None: Path to the .githetic directory, or None if not found
    """
    current = start_dir
    while True:
        git_dir = os.path.join(current, '.githetic')
        if os.path.exists(git_dir) and os.path.isdir(git_dir):
            return git_dir
            
        parent = os.path.dirname(current)
        if parent == current:  # Reached the root directory
            return None
            
        current = parent

def main():
    """Main function to handle command line arguments"""
    args = sys.argv[2:]
    write = False
    file_path = None
    
    
    i = 0
    while i < len(args):
        if args[i] == '-w' or args[i] == '--write':
            write = True
        elif not file_path and not args[i].startswith('-'):
            file_path = args[i]
        i += 1
    
    if not file_path:
        print("Error: No file specified")
        print("Usage: githetic hash-object [-w] <file>")
        sys.exit(1)
    

    sha1 = hash_object(file_path, write)
    print(sha1)

if __name__ == "__main__":
    main()