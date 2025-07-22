import os
import json
import sys

REPO_DIR = ".githetic"

def log():
    

    
    head_path = os.path.join(REPO_DIR, "HEAD")
    if not os.path.exists(head_path):
        print("HEAD introuvable.")
        sys.exit(1)

    with open(head_path, "r") as f:
        current_hash = f.read().strip()

    
    while current_hash:
        commit_path = os.path.join(REPO_DIR, "objects", current_hash, "content.json")
        if not os.path.exists(commit_path):
            print(f"Commit '{current_hash}' introuvable.")
            sys.exit(1)

        with open(commit_path, "r") as f:
            commit = json.load(f)

       
        print(f"commit {current_hash}")
        print(f"Message : {commit.get('message', '(pas de message)')}\n")

        current_hash = commit.get("parent")



if __name__ == "__main__":
    log()