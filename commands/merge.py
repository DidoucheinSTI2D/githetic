import os
import sys
import hashlib
import time
import zlib

def read_object(git_dir, sha):
    obj_path = os.path.join(git_dir, 'objects', sha[:2], sha[2:])
    if not os.path.exists(obj_path):
        return None
    with open(obj_path, 'rb') as f:
        compressed = f.read()
    decompressed = zlib.decompress(compressed)
    return decompressed

def parse_tree(data):
    i = 0
    tree = {}
    while i < len(data):
        space = data.find(b' ', i)
        mode = data[i:space].decode()
        null = data.find(b'\x00', space)
        path = data[space+1:null].decode()
        sha = data[null+1:null+21]
        tree[path] = (mode, sha.hex())
        i = null + 21
    return tree

def write_tree(tree):
    tree_content = b''
    for path in sorted(tree.keys()):
        mode, sha = tree[path]
        entry = f"{mode} {path}".encode() + b'\x00' + bytes.fromhex(sha)
        tree_content += entry
    store = b"tree " + str(len(tree_content)).encode() + b'\x00' + tree_content
    sha = hashlib.sha1(store).hexdigest()
    git_dir = os.path.join(os.getcwd(), '.githetic')
    obj_path = os.path.join(git_dir, 'objects', sha[:2], sha[2:])
    os.makedirs(os.path.dirname(obj_path), exist_ok=True)
    with open(obj_path, 'wb') as f:
        f.write(zlib.compress(store))
    return sha

def commit_merge(tree_hash, parent1, parent2, message):
    commit_content = f"tree {tree_hash}\n"
    commit_content += f"parent {parent1}\n"
    commit_content += f"parent {parent2}\n"
    timestamp = int(time.time())
    commit_content += f"author Githetic <githetic@example.com> {timestamp} +0000\n"
    commit_content += f"committer Githetic <githetic@example.com> {timestamp} +0000\n\n"
    commit_content += message + "\n"
    store = f"commit {len(commit_content)}\0{commit_content}".encode()
    sha = hashlib.sha1(store).hexdigest()
    git_dir = os.path.join(os.getcwd(), '.githetic')
    obj_path = os.path.join(git_dir, 'objects', sha[:2], sha[2:])
    os.makedirs(os.path.dirname(obj_path), exist_ok=True)
    with open(obj_path, 'wb') as f:
        f.write(zlib.compress(store))
    return sha

def merge():
    if len(sys.argv) < 3:
        print("Usage: githetic merge <branch>")
        return

    target_branch = sys.argv[2]
    git_dir = os.path.join(os.getcwd(), '.githetic')
    head_file = os.path.join(git_dir, 'HEAD')

    if not os.path.exists(head_file):
        print("Error: No HEAD found.")
        return

    with open(head_file, 'r') as f:
        ref_line = f.read().strip()

    if not ref_line.startswith("ref: "):
        print("Error: Invalid HEAD")
        return

    current_ref = ref_line[5:]
    current_ref_path = os.path.join(git_dir, current_ref)
    if not os.path.exists(current_ref_path):
        print("Error: HEAD ref does not exist")
        return

    with open(current_ref_path, 'r') as f:
        current_commit = f.read().strip()

    target_ref_path = os.path.join(git_dir, 'refs', 'heads', target_branch)
    if not os.path.exists(target_ref_path):
        print(f"Error: Branch '{target_branch}' does not exist")
        return

    with open(target_ref_path, 'r') as f:
        target_commit = f.read().strip()

    current_commit_data = read_object(git_dir, current_commit).decode()
    target_commit_data = read_object(git_dir, target_commit).decode()

    current_tree_sha = current_commit_data.split('\n')[0].split(' ')[1]
    target_tree_sha = target_commit_data.split('\n')[0].split(' ')[1]

    current_tree_data = read_object(git_dir, current_tree_sha)
    target_tree_data = read_object(git_dir, target_tree_sha)

    current_tree = parse_tree(current_tree_data[tree_data_start(current_tree_data):])
    target_tree = parse_tree(target_tree_data[tree_data_start(target_tree_data):])

    merged_tree = {}
    conflicts = []

    all_files = set(current_tree.keys()).union(target_tree.keys())

    for path in all_files:
        c = current_tree.get(path)
        t = target_tree.get(path)
        if c and t:
            if c[1] == t[1]:
                merged_tree[path] = c  # same hash
            else:
                conflicts.append(path)
        elif c:
            merged_tree[path] = c
        elif t:
            merged_tree[path] = t

    if conflicts:
        print("Merge conflict(s) detected:")
        for path in conflicts:
            print(f"CONFLICT: {path}")
        print("Merge aborted.")
        return

    new_tree_sha = write_tree(merged_tree)
    new_commit_sha = commit_merge(new_tree_sha, current_commit, target_commit, f"Merge branch '{target_branch}'")

    with open(current_ref_path, 'w') as f:
        f.write(new_commit_sha)

    print(f"Merge successful. Created commit {new_commit_sha[:7]}.")

def tree_data_start(data):
    # Finds where the actual tree content starts (after the null byte)
    null_index = data.find(b'\x00')
    return null_index + 1

if __name__ == "__main__":
    merge()
