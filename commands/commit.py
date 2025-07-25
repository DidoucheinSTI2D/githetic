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

    tree_content = b""
    for file_path, hash_value in sorted(entries):
        # Format : mode SP filename NUL SHA1 (20 bytes binary)
        mode = b"100644"
        path_bytes = file_path.encode()
        sha_bytes = bytes.fromhex(hash_value)
        tree_content += mode + b" " + path_bytes + b"\x00" + sha_bytes
    
    header = f"tree {len(tree_content)}\0".encode()
    store = header + tree_content

    tree_hash = hashlib.sha1(store).hexdigest()

    tree_path = os.path.join(objects_dir, tree_hash[:2], tree_hash[2:])
    os.makedirs(os.path.dirname(tree_path), exist_ok=True)
    
    if not os.path.exists(tree_path):
        compressed_content = zlib.compress(store)
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
    
    timestamp = int(time.time())
    author_committer = f"Githetic <githetic@example.com> {timestamp} +0000"

    commit_content = f"tree {tree_hash}\n"
    if parent_hash:
        commit_content += f"parent {parent_hash}\n"
    commit_content += f"author {author_committer}\n"
    commit_content += f"committer {author_committer}\n\n"
    commit_content += f"{message}\n"

    commit_bytes = commit_content.encode()
    header = f"commit {len(commit_bytes)}\0".encode()
    store = header + commit_bytes

    commit_hash = hashlib.sha1(store).hexdigest()
    
    objects_dir = os.path.join(git_dir, 'objects')
    commit_path = os.path.join(objects_dir, commit_hash[:2], commit_hash[2:])
    os.makedirs(os.path.dirname(commit_path), exist_ok=True)
    
    if not os.path.exists(commit_path):
        compressed_content = zlib.compress(store)
        with open(commit_path, 'wb') as f:
            f.write(compressed_content)
    
    refs_heads_main = os.path.join(git_dir, 'refs', 'heads', 'main')
    os.makedirs(os.path.dirname(refs_heads_main), exist_ok=True)
    
    with open(refs_heads_main, 'w') as f:
        f.write(commit_hash)
    
    # Reset index file (clear staged files)
    index_file_path = os.path.join(git_dir, 'index')
    with open(index_file_path, 'w') as f:
        pass
    
    print(f"Created commit {commit_hash[:7]}")

if __name__ == "__main__":
    commit()
