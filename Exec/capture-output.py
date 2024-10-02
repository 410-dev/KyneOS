
# Usage
#    capture-output <memory name> run <command>
#    capture-output <memory name> get

# Captured output is saved at /tmp/capture-output/<memory name>.txt
import System.stdio as stdio
import System.fs as fs
import System.shexec as shexec
from System.Library.execspaces import KernelSpace

def main(args: list, process):
    args.pop(0)  # Remove the script name from args

    if len(args) < 2:
        stdio.println("Usage: capture-output <memory name> run <command>")
        stdio.println("       capture-output <memory name> get")
        return

    memory_name = args[0]
    command = args[2:] if len(args) > 2 else None

    if args[1] == "run":
        if command is None:
            stdio.println("Usage: capture-output <memory name> run <command>")
            return

        # Load tty logs
        currentDisplayTTY = KernelSpace.syscall("drv.io.tty", "getCurrentTTY")
        ttyLog = KernelSpace.syscall("drv.io.tty", "getTTYLog", currentDisplayTTY)

        # Run command
        shexec.interpretParameters(command)

        # New tty logs
        newTTYLog = KernelSpace.syscall("drv.io.tty", "getTTYLog", currentDisplayTTY)

        # Remove old logs from new logs
        output = newTTYLog.replace(ttyLog, "")

        fs.makeDir("/tmp/capture-output")
        fs.writes(f"/tmp/capture-output/{memory_name}.txt", output)

    elif args[1] == "get":
        if not fs.exists(f"/tmp/capture-output/{memory_name}.txt"):
            stdio.println("No output captured for this memory name.")
            return

        output = fs.reads(f"/tmp/capture-output/{memory_name}.txt")
        stdio.println(output)

    else:
        stdio.println("Usage: capture-output <memory name> run <command>")
        stdio.println("       capture-output <memory name> get")
        return
