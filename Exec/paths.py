import System.shexec as shell
import System.stdio as stdio

def main(args: list, process: shell.Process):
    for path in shell.paths(process):
        stdio.println(path)
