import os
import fnmatch

class GitIgnore:
    def __init__(self, repo_root):
        self.repo_root = repo_root
        self.patterns = []
        self.load_patterns()

    def load_patterns(self):
        gitignore_path = os.path.join(self.repo_root, '.gitignore')
        if not os.path.exists(gitignore_path):
            return
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line == '' or line.startswith('#'):
                    continue
                self.patterns.append(line)

    def is_ignored(self, path):
        rel_path = os.path.relpath(path, self.repo_root)
        for pattern in self.patterns:
            if fnmatch.fnmatch(rel_path, pattern):
                return True
            if pattern.endswith('/') and rel_path.startswith(pattern.rstrip('/')):
                return True
        return False
            