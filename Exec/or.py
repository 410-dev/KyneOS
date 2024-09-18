import System.shexec as shell

def main(args: list, process):
    args.pop(0)
    if len(args) < 2:
        return 1
    firstCmd = []
    for i in range(len(args)):
        if args[i] == "||":
            break
        firstCmd.append(args[i])

    secondCmd = []
    for i in range(len(args)):
        if args[i] == "||":
            secondCmd = args[i+1:]
            break

    firstResult = shell.interpretLine(" ".join(firstCmd), process)
    if firstResult == 0:
        return 0
    else:
        result = shell.interpretLine(" ".join(secondCmd), process)
        return result
