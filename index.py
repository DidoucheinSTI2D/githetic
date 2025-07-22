import sys
from commands import test
from commands import init
from commands import hashobject
from commands import catfile
from commands import tree  

def main():
    if len(sys.argv) < 2:
        print("Usage : githetic <command> [options]")
        print("Commands :")
        print("  init : Initialize a new githetic project")
        print("  hash-object : Calculate object ID and optionally create a blob from a file")
        print("  cat-file : Display content of repository objects")
        print("  write-tree : Create a tree object from the current directory")
        print("  add : Add a file to the githetic project")
        print("  commit : Commit the changes to the githetic project")
        print("  push : Push the changes to the githetic project")
        print("  pull : Pull the changes from the githetic project")
        print("  status : Show the status of the githetic project")
        return
    
    command = sys.argv[1]
    if command == "test":
        test.hello()
    elif command == "init":
        init.init()
    elif command == "hash-object":
        hashobject.main()
    elif command == "cat-file":
        catfile.main()
    elif command == "write-tree":
        tree.main()  
    else:
        print(f"Command {command} not found")

if __name__ == "__main__":
    main()
