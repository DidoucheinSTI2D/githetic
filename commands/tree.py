import os
import sys
import hashlib
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
        if parent == current: 
            return None
            
        current = parent

def hash_object(content, obj_type, write=False):
    """Calculate the SHA-1 hash of content and optionally write it to the object store
    
    Args:
        content (bytes): Content to hash
        obj_type (str): Object type (blob, tree, commit, etc.)
        write (bool): Whether to write the object to the object store
        
    Returns:
        str: The SHA-1 hash of the content
    """
   
    header = f"{obj_type} {len(content)}\0".encode()
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

def write_tree(directory=None):
    """Create a tree object from the current directory
    
    Args:
        directory (str, optional): Directory to create tree from. Defaults to current directory.
        
    Returns:
        str: The SHA-1 hash of the created tree object
    """
    if directory is None:
        directory = os.getcwd()
    
  
    git_dir = find_git_dir(directory)
    if not git_dir:
        print("Error: Not a githetic repository (or any of the parent directories)")
        sys.exit(1)
    
    entries = []
    for item in sorted(os.listdir(directory)):
        if item.startswith('.'):
            continue
        
        path = os.path.join(directory, item)
        stat_info = os.stat(path)
        
        if os.path.isdir(path):
            mode = "40000"  
            subtree_hash = write_tree(path)
            entries.append((mode, item, subtree_hash))
        else:
            mode = "100644"  
            with open(path, 'rb') as f:
                content = f.read()
            
            blob_hash = hash_object(content, "blob", write=True)
            entries.append((mode, item, blob_hash))
    
    tree_content = b""
    for mode, name, hash_val in entries:
        
        hash_binary = bytes.fromhex(hash_val)
        
        
        entry = f"{mode} {name}\0".encode() + hash_binary
        tree_content += entry
    
    
    tree_hash = hash_object(tree_content, "tree", write=True)
    return tree_hash

def main():
    """Main function to handle command line arguments"""
    args = sys.argv[2:]
    
    
    tree_hash = write_tree()
    print(tree_hash)

if __name__ == "__main__":
    main()