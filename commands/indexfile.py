import os

INDEX_FILE = ".githetic/index"

def load_index():
    """Charge l’index sous forme d’un dict {filepath: sha1} à partir du fichier texte."""
    index = {}
    if not os.path.exists(INDEX_FILE):
        return index
    with open(INDEX_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(' ', 1)
            if len(parts) == 2:
                sha1, filepath = parts
                index[filepath] = sha1
    return index

def save_index(index_data):
    """Enregistre le dict {filepath: sha1} dans le fichier index au format texte."""
    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    with open(INDEX_FILE, "w") as f:
        for filepath, sha1 in index_data.items():
            f.write(f"{sha1} {filepath}\n")

def add_file_to_index(filepath, sha1):
    """Ajoute ou met à jour une entrée dans l’index."""
    index = load_index()
    index[filepath] = sha1
    save_index(index)
    print(f"Added {filepath} to index.")

def remove_file_from_index(filepath):
    """Supprime une entrée du fichier index."""
    index = load_index()
    if filepath in index:
        del index[filepath]
        save_index(index)
        print(f"Removed {filepath} from index.")
    else:
        print(f"{filepath} not found in index.")
