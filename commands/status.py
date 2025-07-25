import os
import sys
import hashlib
import zlib

def get_file_hash(file_path):
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        return hashlib.sha1(content).hexdigest()
    except:
        return None

def is_file_in_last_commit(file_path):
    current_dir = os.getcwd()
    git_dir = os.path.join(current_dir, '.githetic')
    head_file = os.path.join(git_dir, 'HEAD')
    
    if not os.path.exists(head_file):
        return False
    
    try:
        with open(head_file, 'r') as f:
            head_content = f.read().strip()
            if head_content.startswith('ref: '):
                ref_path = os.path.join(git_dir, head_content[5:])
                if os.path.exists(ref_path):
                    with open(ref_path, 'r') as ref_f:
                        commit_hash = ref_f.read().strip()
                        return is_file_in_commit(file_path, commit_hash, git_dir)
    except:
        pass
    
    return False

def is_file_in_commit(file_path, commit_hash, git_dir):
    try:
        commit_path = os.path.join(git_dir, 'objects', commit_hash[:2], commit_hash[2:])
        if not os.path.exists(commit_path):
            return False
        
        with open(commit_path, 'rb') as f:
            compressed_content = f.read()
        
        commit_content = zlib.decompress(compressed_content).decode()
        
        for line in commit_content.split('\n'):
            if line.startswith('tree '):
                tree_hash = line[5:]
                return is_file_in_tree(file_path, tree_hash, git_dir)
    except:
        pass
    
    return False

def is_file_in_tree(file_path, tree_hash, git_dir):
    try:
        tree_path = os.path.join(git_dir, 'objects', tree_hash[:2], tree_hash[2:])
        if not os.path.exists(tree_path):
            return False
        
        with open(tree_path, 'rb') as f:
            compressed_content = f.read()
        
        tree_content = zlib.decompress(compressed_content).decode('latin1')
        
        # Parser le contenu de l'arbre
        pos = 0
        while pos < len(tree_content):
            # Trouver le prochain null byte
            null_pos = tree_content.find('\x00', pos)
            if null_pos == -1:
                break
            
            # Extraire le mode et le nom
            header = tree_content[pos:null_pos]
            space_pos = header.rfind(' ')
            if space_pos == -1:
                break
            
            mode = header[:space_pos]
            name = header[space_pos + 1:]
            
            if name == file_path:
                return True
            
            # Passer au prochain objet (20 bytes pour le hash)
            pos = null_pos + 21
    except:
        pass
    
    return False

def status():
    """Show staged and unstaged changes"""
    current_dir = os.getcwd()
    git_dir = os.path.join(current_dir, '.githetic')
    
    if not os.path.exists(git_dir):
        print("Error: Not a githetic repository. Run 'githetic init' first.")
        return
    
    index_file = os.path.join(git_dir, 'index')
    
    staged_files = {}
    if os.path.exists(index_file):
        with open(index_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        hash_value, file_path = parts
                        staged_files[file_path] = hash_value
    
    unstaged_changes = []
    untracked_files = []
    
    for root, dirs, files in os.walk('.'):
        if '.githetic' in dirs:
            dirs.remove('.githetic')
        
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.startswith('./'):
                file_path = file_path[2:]
            
            current_hash = get_file_hash(file_path)
            
            if file_path in staged_files:
                if current_hash != staged_files[file_path]:
                    unstaged_changes.append(file_path)
            else:
                if not is_file_in_last_commit(file_path):
                    untracked_files.append(file_path)

    print("On branch main")
    print()
    
    if staged_files:
        print("Changes to be committed:")
        print("  (use \"githetic commit -m <message>\" to commit)")
        print()
        for file_path in sorted(staged_files.keys()):
            print(f"        new file:   {file_path}")
        print()
    
    if unstaged_changes:
        print("Changes not staged for commit:")
        print("  (use \"githetic add <file>...\" to update what will be committed)")
        print()
        for file_path in sorted(unstaged_changes):
            print(f"        modified:   {file_path}")
        print()
    
    if untracked_files:
        print("Untracked files:")
        print("  (use \"githetic add <file>...\" to include in what will be committed)")
        print()
        for file_path in sorted(untracked_files):
            print(f"        {file_path}")
        print()
    
    if not staged_files and not unstaged_changes and not untracked_files:
        print("nothing to commit, working tree clean")

if __name__ == "__main__":
    status() 