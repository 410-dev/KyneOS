import importlib
import asyncio
import threading
import ctypes
import time
import os
import inspect
import System.Library.CoreInfrastructures.journaling as Journaling
from typing import Any, Callable
# from system.kernel.v100.modules import process as process_module


class Process:
    def __init__(self, name: str, executable: str, arguments: list[str], ownerUser) -> None:
        from System.Library.CoreInfrastructures.Objects.User import User
        self.pid: int = -1
        self.name: str = name
        self.executable: str = executable
        self.executableModule: str = executable.replace(".py", "").replace("/", ".").replace(os.path.sep, ".")
        if self.executableModule.startswith("."):
            self.executableModule = self.executableModule[1:]
        self.arguments: list[str] = arguments
        self.ownerUser: User = ownerUser
        self.ownerProcess = None
        self.ownerProcess: "Process" = self.getOwnerProcess()

        self.module = None
        self.thread = None
        self.launchedSync: bool = False
        self.isRunning: bool = False

        # Display the process creation details
        if self.ownerProcess:
            print(f"Process '{self.name}' created. Owned by: '{self.ownerProcess.name}'")
        else:
            print(f"Process '{self.name}' created as a Kernel Process.")


    def getOwnerProcess(self) -> "Process":
        if not self.ownerProcess or not self.ownerProcess.isRunning:
            stack = inspect.stack()
            for frame_info in stack:
                frame_locals = frame_info.frame.f_locals
                if 'self' in frame_locals:
                    caller_self = frame_locals['self']

                    if isinstance(caller_self, Process):
                        if caller_self.pid == self.pid:
                            continue
                        print(f"Owner process found: {caller_self.name} for pid {caller_self.pid}")
                        return caller_self
                        # continue

        # If no Process instance is found, return self (Kernel Process)
        return self

    def _load_module(self):
        self.module = importlib.reload(importlib.import_module(self.executableModule))

    def kill(self, code: int) -> bool:
        if not self.launchedSync and self.loop and self.thread:
            if hasattr(self.module, 'terminateAsync'):
                future = asyncio.run_coroutine_threadsafe(self._graceful_terminate_async(code), self.loop)
                try:
                    future.result(timeout=5)  # Wait for up to 5 seconds
                except asyncio.TimeoutError:
                    Journaling.record("TIMEOUT", f"Async termination timed out after 5 seconds.")
                except Exception as e:
                    Journaling.record("ERROR", f"Error in async termination: {e}")
            else:
                Journaling.record("INFO", f"No terminateAsync method found for async process.")

            if not self.launchedSync:
                self._force_terminate()

        elif self.launchedSync:
            if hasattr(self.module, 'terminate'):
                try:
                    self.module.terminate(code)
                except Exception as e:
                    Journaling.record("ERROR", f"Error in sync termination: {e}")
            else:
                Journaling.record("INFO", f"No terminate method found for sync process.")

        self.isRunning = False

        if self.thread:
            self.thread.join(timeout=1)  # Wait for up to 1 second for the thread to finish

        if self.thread and self.thread.is_alive():
            return False

        return True

    def launchSync(self, args: Any) -> int:
        from System.Library.CoreInfrastructures.execspaces import UserSpace
        self._load_module()
        self.pid = UserSpace.nextPID()
        self.launchedSync = True

        exitCode = 1
        try:
            UserSpace.registerProcess(self)
            self.isRunning = True
            Journaling.record("INFO", f"Process {self.pid} started.")
            exitCode = self.module.main(args, self)
            self.processEnd(exitCode)
            self.isRunning = False
            return exitCode
        except Exception as e:
            import traceback
            traceback.print_exc()
            Journaling.record("ERROR", f"Process terminated with exit code: {exitCode} - {e}")
            return 1


    def processEnd(self, exitCode: int) -> None:
        self.isRunning = False
        Journaling.record("INFO", f"Process terminated with exit code: {exitCode}")
        # Add any additional cleanup or notification logic here


    ## ASYNC PROCESS LAUNCHING
    async def _wrapped_main(self, args: Any, process: "Process"):
        try:
            self.launchedSync = False
            self.isRunning = True
            await self.module.mainAsync(args, process)
        finally:
            self.isRunning = False

    def _run_async_loop(self, args: Any, process: "Process"):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        try:
            self.loop.run_until_complete(self._wrapped_main(args, process))
        except asyncio.CancelledError:
            pass
        finally:
            self.loop.close()
            self.processEnd(0)

    def launchAsync(self, args: Any) -> int:
        from System.Library.CoreInfrastructures.execspaces import UserSpace
        self._load_module()
        self.pid = UserSpace.nextPID()
        self.launchedSync = False

        UserSpace.registerProcess(self)
        self.thread = threading.Thread(target=self._run_async_loop, args=(args, self))
        self.thread.start()
        Journaling.record("INFO", f"Process {self.pid} started.")

        return self.pid

    def _async_raise(self, tid, exctype):
        if not inspect.isclass(exctype):
            raise TypeError("Only types can be raised (not instances)")
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("Invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    async def _graceful_terminate_async(self, code: int):
        try:
            Journaling.record("INFO", f"Starting async termination...")
            await self.module.terminateAsync(code)
            Journaling.record("INFO", f"Async termination completed.")
        except Exception as e:
            Journaling.record("ERROR", f"Error in graceful async termination: {e}")

    def _force_terminate(self):
        self.loop.call_soon_threadsafe(self.loop.stop)

        start_time = time.time()
        while (not self.launchedSync and self.isRunning) and time.time() - start_time < 1:
            time.sleep(0.1)

        if self.launchedSync and self.isRunning:
            try:
                self._async_raise(self.thread.ident, SystemExit)
            except ValueError:
                pass  # Thread already finished