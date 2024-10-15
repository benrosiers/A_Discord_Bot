# A/bot/bot.py

"""
File: bot.py
Path: A/bot/bot.py
Author: Benoit Desrosiers
Date: 06-04-23
Description: Defines the Bot class for the Discord bot application.
"""

import discord
from discord.ext import commands
from config.settings import COMMAND_PREFIX


class Bot(commands.Bot):
    """
    A subclass of commands.Bot representing the Discord bot.
    """

    def __init__(self):
        """
        Initialize the bot with all intents and set up the command prefix.
        """
        intents = discord.Intents.all()
        super().__init__(command_prefix=COMMAND_PREFIX, intents=intents)

    async def setup_hook(self):
        """
        Called when the bot is setting up; load extensions here.
        """
        await self.load_extension("bot.cogs.voice")

    async def on_ready(self):
        """
        Called when the bot is ready.
        """
        print(f'Bot has connected to Discord as {self.user}!')
