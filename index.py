import sys
from commands import test
from commands import init
from commands import hashobject
from commands import catfile
from commands import tree  
from commands import add
from commands import rm
from commands import commit
from commands import status

def main():
    if len(sys.argv) < 2:
        print("Usage : githetic <command> [options]")
        print("Commands :")
        print("  init : Initialize a new githetic project")
        print("  hash-object : Calculate object ID and optionally create a blob from a file")
        print("  cat-file : Display content of repository objects")
        print("  write-tree : Create a tree object from the current directory")
        print("  add : Add a file to the githetic project")
        print("  rm : Remove a file from working directory and index")
        print("  commit : Commit the changes to the githetic project")
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
    elif command == "add":
        add.add()
    elif command == "rm":
        rm.rm()
    elif command == "commit":
        commit.commit()
    elif command == "status":
        status.status()
    else:
        print(f"Command {command} not found")

if __name__ == "__main__":
    main()
