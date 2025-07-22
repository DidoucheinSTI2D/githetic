import os
import sys
import zlib

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

def cat_file(object_hash, option):
    """Display the content of a Git object
    
    Args:
        object_hash (str): The SHA-1 hash of the object to display
        option (str): The option to use (p: pretty-print, t: show type, s: show size)
        
    Returns:
        None
    """

    current_dir = os.getcwd()
    git_dir = find_git_dir(current_dir)
    if not git_dir:
        print("Error: Not a githetic repository (or any of the parent directories)")
        sys.exit(1)
    
    # Find the object file
    object_dir = os.path.join(git_dir, 'objects', object_hash[:2])
    object_path = os.path.join(object_dir, object_hash[2:])
    
    if not os.path.exists(object_path):
        print(f"Error: Object '{object_hash}' not found")
        sys.exit(1)
    
    try:
        # Read and decompress the object
        with open(object_path, 'rb') as f:
            compressed_content = f.read()
        
        content = zlib.decompress(compressed_content)
        
        # Parse the object header
        # Format: "type size\0content"
        header_end = content.find(b'\0')
        if header_end == -1:
            print("Error: Invalid object format")
            sys.exit(1)
        
        header = content[:header_end].decode('utf-8')
        parts = header.split(' ')
        if len(parts) != 2:
            print("Error: Invalid object header")
            sys.exit(1)
        
        obj_type, obj_size = parts
        obj_content = content[header_end + 1:]
        
        # Display based on the option
        if option == 'p':  # pretty-print
            try:
                # Try to decode as UTF-8, but fall back to binary if it fails
                print(obj_content.decode('utf-8'), end='')
            except UnicodeDecodeError:
                print(f"Binary content, {len(obj_content)} bytes")
        elif option == 't':  # show type
            print(obj_type)
        elif option == 's':  # show size
            print(obj_size)
        else:
            print(f"Error: Unknown option '{option}'")
            print("Usage: githetic cat-file [-p|-t|-s] <object>")
            sys.exit(1)
    
    except Exception as e:
        print(f"Error reading object: {e}")
        sys.exit(1)

def main():
    """Main function to handle command line arguments"""
    args = sys.argv[2:]
    
    if len(args) != 2:
        print("Error: Invalid arguments")
        print("Usage: githetic cat-file [-p|-t|-s] <object>")
        sys.exit(1)
    
    option = args[0]
    if not option.startswith('-') or len(option) != 2:
        print("Error: Invalid option")
        print("Usage: githetic cat-file [-p|-t|-s] <object>")
        sys.exit(1)
    
    option = option[1:]  # Remove the '-'
    object_hash = args[1]
    
    cat_file(object_hash, option)

if __name__ == "__main__":
    main()