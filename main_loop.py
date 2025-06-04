# main.py
import asyncio
import mai  # ← points at your existing code

async def main():
    # Call your old, synchronous run_game() inside an async wrapper.
    # We immediately relinquish control each frame by `await asyncio.sleep(0)`.
    # (Pygbag needs that so the WebAssembly event loop can drive the browser.)
    #
    # One easy pattern is just to kick off your existing loop in a thread-like fashion:
    loop_task = asyncio.to_thread(game_loop.run_game)
    try:
        # Let your game‐loop run "synchronously" on a background thread,
        # and keep this async function alive so that WebGL/VSync can tick.
        while True:
            await asyncio.sleep(0)
    finally:
        # (If you ever want to shut everything down, cancel the thread task.)
        loop_task.cancel()

# This is exactly what pygbag expects:
asyncio.run(main())

# Note: do NOT put any code after asyncio.run(main())—pygbag’s loader will never run it.