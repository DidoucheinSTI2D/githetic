import sys
from commands import test
from commands import init

def main():
    if len(sys.argv) < 2:
        print("Usage : githetic <command> [options]")
        print("Commands :")
        print("  init : Initialize a new githetic project")
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
    else:
        print(f"Command {command} not found")

if __name__ == "__main__":
    main()
