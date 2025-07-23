import sys
from commands import test
from commands import init
from commands import add
from commands import rm
from commands import commit
from commands import status
from commands import checkout
from commands import reset
from commands import log

def main():
    if len(sys.argv) < 2:
        print("Usage : githetic <command> [options]")
        print("Commands :")
        print("  init     : Initialize a new githetic project")
        print("  add      : Add a file to the githetic project")
        print("  rm       : Remove a file from working directory and index")
        print("  commit   : Commit the changes to the githetic project")
        print("  status   : Show the status of the githetic project")
        print("  checkout : Switch to a specific commit or branch")
        print("  reset    : Reset HEAD and index to a specific commit")
        print("  log      : Show commit history")
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
    elif command == "checkout":
        if len(sys.argv) < 3:
            print("Usage : githetic checkout <commit_or_branch>")
            return
        ref = sys.argv[2]
        checkout.checkout(ref)
    elif command == "reset":
        if len(sys.argv) < 3:
            print("Usage : githetic reset <commit>")
            return
        ref = sys.argv[2]
        reset.reset(ref)
    elif command == "log":
        log.log()
    else:
        print(f"Command {command} not found")

if __name__ == "__main__":
    main()