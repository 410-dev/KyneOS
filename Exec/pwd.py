from System.Library.Objects.Process import Process
import System.stdio as stdio

def main(args: list, process: Process):
    stdio.println(process.cwd)
