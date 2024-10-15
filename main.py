# A/main.py

"""
File: main.py
Path: A/main.py
Author: Benoit Desrosiers
Date: 06-04-23
Description: Main entry point for the Discord bot application.
"""

import logging
import sys
import asyncio
import threading
import time
from bot.bot import Bot
from config.settings import BOT_TOKEN
from pynput import keyboard

# Event to signal when Ctrl-Q is pressed
shutdown_event = threading.Event()

# Variable to keep track of the last displayed message time
last_display_time = 0

def setup_logging():
    """
    Set up logging for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
    )

def display_quit_message():
    """
    Display "Press ctrl-q to quit" message if not displayed in the last 20 seconds.
    """
    global last_display_time
    current_time = time.time()
    if current_time - last_display_time >= 20:
        print("Press ctrl-q to quit")
        last_display_time = current_time

def keyboard_listener():
    """
    Listen for Ctrl-Q keypress and set the shutdown_event when detected.
    """
    def on_press(key):
        """
        Handle key press events.
        """
        pass  # We only need to handle key releases

    def on_release(key):
        """
        Handle key release events.
        """
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            # Control key released; nothing to do
            pass
        elif key == keyboard.KeyCode.from_char('q'):
            # 'q' key released; check if control is pressed
            if any([keyboard.Controller().pressed(keyboard.Key.ctrl_l),
                    keyboard.Controller().pressed(keyboard.Key.ctrl_r)]):
                # Ctrl-Q detected
                shutdown_event.set()
                return False  # Stop listener

    # Start the keyboard listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

async def shutdown_bot(bot):
    """
    Gracefully shut down the bot.

    Args:
        bot (Bot): The bot instance.
    """
    # Disconnect from voice channels
    for vc in bot.voice_clients:
        if vc.is_connected():
            await vc.disconnect()

    # Close the bot
    await bot.close()

async def periodic_task(bot):
    """
    Periodic task to display the quit message and check for shutdown event.

    Args:
        bot (Bot): The bot instance.
    """
    while not shutdown_event.is_set():
        display_quit_message()
        await asyncio.sleep(1)  # Check every second for responsiveness

    # Shutdown event is set; proceed to shut down the bot
    await shutdown_bot(bot)

async def main():
    """
    Main function to run the Discord bot.
    """
    setup_logging()
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is not set. Please set it as an environment variable.")
        sys.exit(1)

    # Create the bot instance
    bot = Bot()

    # Start the keyboard listener in a separate thread
    keyboard_thread = threading.Thread(target=keyboard_listener, daemon=True)
    keyboard_thread.start()

    # Run the periodic task in the event loop
    asyncio.create_task(periodic_task(bot))

    # Run the bot
    try:
        await bot.start(BOT_TOKEN)
    except KeyboardInterrupt:
        # Handle Ctrl-C gracefully
        logging.info("Bot is shutting down due to keyboard interrupt.")
        await shutdown_bot(bot)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        # Ensure the bot is closed properly
        if not bot.is_closed():
            await shutdown_bot(bot)

if __name__ == "__main__":
    asyncio.run(main())
