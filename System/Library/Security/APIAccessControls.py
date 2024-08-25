import inspect
import os


def isAccessFromScope(path: str, offset: int = 0) -> bool:
    caller_path = getCallerScriptLocation(offset + 1)
    return caller_path.startswith(path)

def getCallerScriptLocation(offset: int = 0) -> str:
    stack = inspect.stack()
    caller_frame = stack[2 + offset]
    caller_module_path = os.path.abspath(caller_frame.frame.f_globals['__file__'])

    # Convert the absolute path to a Python module-like path
    caller_module_path = os.path.relpath(caller_module_path, os.getcwd())
    caller_module_path = caller_module_path.replace(os.path.sep, '.')
    if caller_module_path.endswith('.py'):
        caller_module_path = caller_module_path[:-3]  # remove the .py extension
    return caller_module_path
