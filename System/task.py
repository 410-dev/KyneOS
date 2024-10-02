import inspect

def getProcess():
    frame = inspect.currentframe()
    process = None
    callerFunctionTraces = []
    while frame:
        frame_info = inspect.getframeinfo(frame)
        callerFunctionTraces.append(frame_info.function)
        filename = frame_info.filename.replace("\\", "/")
        if 'System/Library/Objects/Process.py' in filename:
            # Now check for any instance of the Process class in the local variables
            local_vars = frame.f_locals
            process = local_vars.get('self')  # This should get process object
            break
        else:
            # Move to the previous frame in the call stack
            frame = frame.f_back

    return process
