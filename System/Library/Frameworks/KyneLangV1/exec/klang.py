import System.stdio as stdio

def main(args: list, process):
    args.pop(0)

    if len(args) == 0:
        stdio.println("Usage: klang [sync/async] [scriptfile] <args>")
        stdio.println("Example: klang async example.sc arg1 arg2")
