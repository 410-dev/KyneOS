import System.stdio as stdio

def main(args: list, process):
    args.pop(0)
    stdio.println(" ".join(args))
