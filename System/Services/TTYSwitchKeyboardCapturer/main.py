# import asyncio
#
# from pynput import keyboard
#
# listener = None
#
async def mainAsync(args: list, process):
    pass
#     current = set()
#     def on_press(key):
#         SwitchTTYF2 = {keyboard.Key.shift, keyboard.Key.f2}
#         if key in SwitchTTYF2:
#             current.add(key)
#             if all(k in current for k in SwitchTTYF2):
#                 print('TTY should switch now!!!')
#         if key == keyboard.Key.esc:
#             asyncio.run(terminateAsync(0))
#
#     def on_release(key):
#         try:
#             current.remove(key)
#         except KeyError:
#             pass
#
#     global listener
#     listener = keyboard.Listener(on_press=on_press, on_release=on_release)
#     listener.start()
#     listener.join()
#
# async def terminateAsync(code: int):
#     global listener
#     listener.stop()
