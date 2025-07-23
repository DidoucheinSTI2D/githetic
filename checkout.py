import os
import json
import sys

REPO_DIR = ".githetic"

def checkout(ref):
    

    
    ref_path = os.path.join(REPO_DIR, "refs", "heads", ref)
    if os.path.exists(ref_path):
        with open(ref_path, "r") as f:
            commit_hash = f.read().strip()
    
    elif len(ref) == 40 and all(c in "0123456789abcdef" for c in ref):
        commit_hash = ref
    else:
        print(f"Référence '{ref}' introuvable.")
        sys.exit(1)

    
    commit_path = os.path.join(REPO_DIR, "objects", commit_hash, "content.json")
    if not os.path.exists(commit_path):
        print(f"Commit '{commit_hash}' introuvable.")
        sys.exit(1)
    with open(commit_path, "r") as f:
        commit = json.load(f)

   
    tree_hash = commit["tree"]
    tree_path = os.path.join(REPO_DIR, "objects", tree_hash, "content.json")
    if not os.path.exists(tree_path):
        print(f"Arbre '{tree_hash}' introuvable.")
        sys.exit(1)
    with open(tree_path, "r") as f:
        tree = json.load(f)

    
    for entry in tree["entries"]:
        if entry["type"] != "blob":
            continue  

        blob_hash = entry["hash"]
        blob_path = os.path.join(REPO_DIR, "objects", blob_hash, "content.json")
        if not os.path.exists(blob_path):
            print(f"Blob '{blob_hash}' introuvable.")
            sys.exit(1)
        with open(blob_path, "r") as f:
            blob = json.load(f)

        
        with open(entry["name"], "w") as file:
            file.write(blob["content"])

    
    with open(os.path.join(REPO_DIR, "HEAD"), "w") as f:
        f.write(commit_hash)

    print(f"Checkout effectué avec succès vers le commit {commit_hash[:7]}")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python checkout.py <ref>")
        sys.exit(1)

    ref = sys.argv[1]
    checkout(ref)