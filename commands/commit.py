import os
import sys
import hashlib
import time
import zlib

def write_tree():
    current_dir = os.getcwd()
    git_dir = os.path.join(current_dir, '.githetic')
    index_file = os.path.join(git_dir, 'index')
    objects_dir = os.path.join(git_dir, 'objects')
    
    if not os.path.exists(index_file):
        return None
    
    entries = []
    with open(index_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    hash_value, file_path = parts
                    entries.append((file_path, hash_value))
    
    if not entries:
        return None

    tree_content = ""
    for file_path, hash_value in sorted(entries):
        tree_content += f"100644 {file_path}\x00{bytes.fromhex(hash_value)}"
    
    tree_hash = hashlib.sha1(tree_content.encode('latin1')).hexdigest()

    tree_path = os.path.join(objects_dir, tree_hash[:2], tree_hash[2:])
    os.makedirs(os.path.dirname(tree_path), exist_ok=True)
    
    compressed_content = zlib.compress(tree_content.encode('latin1'))
    with open(tree_path, 'wb') as f:
        f.write(compressed_content)
    
    return tree_hash

def commit():
    if len(sys.argv) < 4 or sys.argv[2] != '-m':
        print("Usage: githetic commit -m \"message\"")
        return
    
    message = sys.argv[3]
    current_dir = os.getcwd()
    git_dir = os.path.join(current_dir, '.githetic')
    
    if not os.path.exists(git_dir):
        print("Error: Not a githetic repository. Run 'githetic init' first.")
        return
    
    tree_hash = write_tree()
    if not tree_hash:
        print("Error: No files staged for commit")
        return
    
    head_file = os.path.join(git_dir, 'HEAD')
    parent_hash = None
    if os.path.exists(head_file):
        with open(head_file, 'r') as f:
            head_content = f.read().strip()
            if head_content.startswith('ref: '):
                ref_path = os.path.join(git_dir, head_content[5:])
                if os.path.exists(ref_path):
                    with open(ref_path, 'r') as ref_f:
                        parent_hash = ref_f.read().strip()
    
    commit_content = f"tree {tree_hash}\n"
    if parent_hash:
        commit_content += f"parent {parent_hash}\n"
    
    commit_content += f"author Githetic <githetic@example.com> {int(time.time())} +0000\n"
    commit_content += f"committer Githetic <githetic@example.com> {int(time.time())} +0000\n\n"
    commit_content += f"{message}\n"
    
    commit_hash = hashlib.sha1(commit_content.encode()).hexdigest()
    
    objects_dir = os.path.join(git_dir, 'objects')
    commit_path = os.path.join(objects_dir, commit_hash[:2], commit_hash[2:])
    os.makedirs(os.path.dirname(commit_path), exist_ok=True)
    
    compressed_content = zlib.compress(commit_content.encode())
    with open(commit_path, 'wb') as f:
        f.write(compressed_content)
    
    refs_heads_main = os.path.join(git_dir, 'refs', 'heads', 'main')
    os.makedirs(os.path.dirname(refs_heads_main), exist_ok=True)
    
    with open(refs_heads_main, 'w') as f:
        f.write(commit_hash)
    
    index_file_path = os.path.join(git_dir, 'index')
    with open(index_file_path, 'w') as f:
        pass
    
    print(f"Created commit {commit_hash[:7]}")

if __name__ == "__main__":
    commit() 