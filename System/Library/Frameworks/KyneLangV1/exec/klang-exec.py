import System.stdio as stdio


def main(args: list, process):
    args.pop(0)

    if len(args) == 0:
        stdio.println("Usage: klang-exec [sync/async] [script]")
        stdio.println("Example: klang-exec async print hello world")
