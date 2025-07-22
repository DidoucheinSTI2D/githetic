import sys
from commands import test
from commands import init
from commands import add
from commands import rm
from commands import commit
from commands import status

def main():
    if len(sys.argv) < 2:
        print("Usage : githetic <command> [options]")
        print("Commands :")
        print("  init : Initialize a new githetic project")
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
