import os
import json
import sys

REPO_DIR = ".githetic"

def reset(commit_hash):

    
    commit_path = os.path.join(REPO_DIR, "objects", commit_hash, "content.json")
    if not os.path.exists(commit_path):
        print(f"Commit '{commit_hash}' introuvable.")
        sys.exit(1)

    
    with open(commit_path, "r") as f:
        commit = json.load(f)

    
    tree_hash = commit.get("tree")
    tree_path = os.path.join(REPO_DIR, "objects", tree_hash, "content.json")
    if not os.path.exists(tree_path):
        print(f"Arbre '{tree_hash}' introuvable.")
        sys.exit(1)

    
    with open(tree_path, "r") as f:
        tree = json.load(f)

    
    index_entries = []
    for entry in tree.get("entries", []):
        if entry.get("type") == "blob":
            index_entries.append(f"{entry['hash']} {entry['name']}")

    index_path = os.path.join(REPO_DIR, "index")
    with open(index_path, "w") as f:
        f.write("\n".join(index_entries))

    
    head_path = os.path.join(REPO_DIR, "HEAD")
    with open(head_path, "w") as f:
        f.write(commit_hash)

    print(f"Reset effectué : HEAD repositionné vers le commit {commit_hash[:7]}")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python reset.py <commit_hash>")
        sys.exit(1)

    commit_hash = sys.argv[1]
    reset(commit_hash)