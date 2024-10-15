# A/bot/cogs/voice.py

"""
File: voice.py
Path: A/bot/cogs/voice.py
Author: Benoit Desrosiers
Date: 06-04-23
Description: Cog for handling voice commands and functionalities.
"""

import discord
from discord.ext import commands, tasks
from utils.audio import AudioUtils
import asyncio
import logging
import time


class Voice(commands.Cog):
    """
    Cog for handling voice-related commands.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the Voice cog.

        Args:
            bot (commands.Bot): The bot instance.
        """
        self.bot = bot
        self.inactivity_timeout = 60  # Timeout in seconds (1 minute)
        self.voice_clients = {}
        self.check_inactivity.start()

    def cog_unload(self):
        """
        Called when the cog is unloaded. Cancels the inactivity check task.
        """
        self.check_inactivity.cancel()

    @commands.command(name='say')
    async def say(self, ctx: commands.Context, *, text: str):
        """
        Command for the bot to speak the given text in a voice channel.

        The bot will attempt to speak in:
        1. The voice channel the message author is in.
        2. The first voice channel with someone in it.
        3. The first voice channel of the server.

        Args:
            ctx (commands.Context): The context in which the command was invoked.
            text (str): The text for the bot to convert to speech.
        """
        voice_channel = await self.get_voice_channel(ctx)

        if voice_channel is None:
            await ctx.send("No voice channels available.")
            return

        # Connect to the voice channel if not already connected
        voice_client = ctx.voice_client
        if not voice_client:
            try:
                voice_client = await voice_channel.connect()
            except discord.DiscordException as e:
                await ctx.send(f"Failed to connect to voice channel: {e}")
                return
        elif voice_client.channel != voice_channel:
            try:
                await voice_client.move_to(voice_channel)
            except discord.DiscordException as e:
                await ctx.send(f"Failed to move to voice channel: {e}")
                return

        # Update the last active time
        self.voice_clients[voice_client] = time.monotonic()

        # Generate in-memory audio
        audio_stream = AudioUtils.generate_audio(text)

        if audio_stream:
            # Play the audio stream
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(
                    audio_stream,
                    pipe=True,
                    options='-loglevel panic -hide_banner -nostats -vn -analyzeduration 0',
                )
            )
            try:
                def after_playing(error):
                    if error:
                        logging.error(f"Error in voice playback: {error}")
                    else:
                        # Schedule the update in the main event loop
                        self.bot.loop.call_soon_threadsafe(self.update_last_active, voice_client)

                voice_client.play(source, after=after_playing)
                await ctx.send(f"Speaking in {voice_channel.name}")
            except discord.DiscordException as e:
                await ctx.send(f"Failed to play audio: {e}")
        else:
            await ctx.send("Failed to generate audio.")

    def update_last_active(self, voice_client):
        """
        Update the last active time for a voice client.

        Args:
            voice_client (discord.VoiceClient): The voice client to update.
        """
        self.voice_clients[voice_client] = time.monotonic()

    @commands.command(name='saynomore')
    async def saynomore(self, ctx: commands.Context):
        """
        Command to make the bot say "Bye" and disconnect from the voice channel.

        Args:
            ctx (commands.Context): The context in which the command was invoked.
        """
        voice_client = ctx.voice_client
        if not voice_client:
            await ctx.send("I am not connected to any voice channel.")
            return

        # Generate in-memory audio for "Bye"
        audio_stream = AudioUtils.generate_audio("Bye")

        if audio_stream:
            # Play the audio stream
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(
                    audio_stream,
                    pipe=True,
                    options='-loglevel panic -hide_banner -nostats -vn -analyzeduration 0',
                )
            )
            try:
                def after_playing(error):
                    if error:
                        logging.error(f"Error in voice playback: {error}")
                    else:
                        # Schedule the disconnection in the main event loop
                        self.bot.loop.call_soon_threadsafe(self.disconnect_voice_client, voice_client)

                voice_client.play(source, after=after_playing)
                await ctx.send("Goodbye!")
            except discord.DiscordException as e:
                await ctx.send(f"Failed to play audio: {e}")
        else:
            await ctx.send("Failed to generate 'Bye' audio.")

    def disconnect_voice_client(self, voice_client):
        """
        Disconnect a voice client.

        Args:
            voice_client (discord.VoiceClient): The voice client to disconnect.
        """
        coro = voice_client.disconnect()
        asyncio.ensure_future(coro, loop=self.bot.loop)
        if voice_client in self.voice_clients:
            del self.voice_clients[voice_client]

    async def get_voice_channel(self, ctx: commands.Context) -> discord.VoiceChannel:
        """
        Determine the voice channel to use based on the author's status and server state.

        Args:
            ctx (commands.Context): The context in which the command was invoked.

        Returns:
            discord.VoiceChannel or None: The voice channel to use, or None if not found.
        """
        # 1. Check if the author is in a voice channel
        if ctx.author.voice:
            return ctx.author.voice.channel
        else:
            # 2. Find the first voice channel with someone in it
            for vc in ctx.guild.voice_channels:
                if len(vc.members) > 0:
                    return vc

            # 3. If no one is in any voice channel, use the first voice channel
            if ctx.guild.voice_channels:
                return ctx.guild.voice_channels[0]

        return None

    @tasks.loop(seconds=30)
    async def check_inactivity(self):
        """
        Periodically checks for inactive voice clients and disconnects them after a timeout.
        """
        current_time = time.monotonic()
        to_disconnect = []
        for voice_client, last_active in self.voice_clients.items():
            if not voice_client.is_playing() and current_time - last_active > self.inactivity_timeout:
                to_disconnect.append(voice_client)

        for voice_client in to_disconnect:
            # Generate in-memory audio for "Bye"
            audio_stream = AudioUtils.generate_audio("Bye")
            if audio_stream:
                source = discord.PCMVolumeTransformer(
                    discord.FFmpegPCMAudio(
                        audio_stream,
                        pipe=True,
                        options='-loglevel panic -hide_banner -nostats -vn -analyzeduration 0',
                    )
                )
                try:
                    def after_playing(error):
                        if error:
                            logging.error(f"Error in voice playback: {error}")
                        else:
                            # Schedule the disconnection in the main event loop
                            self.bot.loop.call_soon_threadsafe(self.disconnect_voice_client, voice_client)

                    voice_client.play(source, after=after_playing)
                except discord.DiscordException as e:
                    logging.error(f"Failed to play 'Bye' audio: {e}")
                    await voice_client.disconnect()
                    if voice_client in self.voice_clients:
                        del self.voice_clients[voice_client]
            else:
                logging.error("Failed to generate 'Bye' audio.")
                await voice_client.disconnect()
                if voice_client in self.voice_clients:
                    del self.voice_clients[voice_client]

    @check_inactivity.before_loop
    async def before_check_inactivity(self):
        """
        Wait until the bot is ready before starting the inactivity check loop.
        """
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    """
    The asynchronous setup function to load this cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(Voice(bot))
