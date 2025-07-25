import os
import sys

def init():
    """Initialize a new githetic repository"""
    current_dir = os.getcwd()
    git_dir = os.path.join(current_dir, '.githetic')
    
    if os.path.exists(git_dir):
        print(f"Reinitialized existing githetic repository in {current_dir}")
        return
    
    try:
        os.makedirs(git_dir)
        
        os.makedirs(os.path.join(git_dir, 'objects'))
        os.makedirs(os.path.join(git_dir, 'refs', 'heads'))
        os.makedirs(os.path.join(git_dir, 'refs', 'tags'))
        
        with open(os.path.join(git_dir, 'HEAD'), 'w') as head_file:
            head_file.write('ref: refs/heads/main\n')

        with open(os.path.join(git_dir, 'config'), 'w') as config_file:
            config_file.write('[core]\n')
            config_file.write('\trepositoryformatversion = 0\n')
            config_file.write('\tfilemode = true\n')
            config_file.write('\tbare = false\n')
            config_file.write('\tlogallrefupdates = true\n')
        
        with open(os.path.join(git_dir, 'description'), 'w') as desc_file:
            desc_file.write('Unnamed repository; edit this file \'description\' to name the repository.\n')
        
        open(os.path.join(git_dir, 'index'), 'w').close()
        
        print(f"Initialized empty githetic repository in {os.path.join(current_dir, '.githetic/')}")
        
    except OSError as e:
        print(f"Error: Could not initialize githetic repository: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init() 