import io
import logging
import os
from datetime import datetime

import aiohttp
import discord
import requests
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv
from pytz import timezone

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.Formatter.converter = lambda *args: datetime.now(
    tz=timezone("Asia/Kolkata")
).timetuple()
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
FLAG = os.getenv("FLAG")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)
client = discord.Client(intents=intents)


@bot.event
async def on_ready():
    logging.info(f"logged in as {bot.user.name} ({bot.user.id})")
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="with life"))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return


@bot.hybrid_command()
async def sendmessage(ctx, link):
    if isinstance(ctx.channel, discord.channel.TextChannel):
        if ctx.author.guild_permissions.administrator:
            channel = ctx.channel
            try:
                if link.startswith("http://") or link.startswith("https://"):
                    response = requests.get(link)
                    if response.status_code == 200:
                        content = response.text
                        await channel.send(content)
                        await ctx.send("Message sent successfully.", ephemeral=True)
                        logging.info(f"message sent by {ctx.author.name}")
                    else:
                        await ctx.send(
                            "Failed to fetch the content from the provided link.",
                            ephemeral=True,
                        )
                else:
                    await channel.send(link)
                    await ctx.send("Message sent successfully.", ephemeral=True)
                    logging.info(f"message sent by {ctx.author.name}")
            except Exception as e:
                await ctx.send(f"An error occurred: {e}", ephemeral=True)
                logging.warning(f"error occurred: {e}")
        else:
            await ctx.send(
                "You don't have permissions to send the message.", ephemeral=True
            )


@bot.hybrid_command()
async def editmessage(ctx, link, message_id):
    if isinstance(ctx.channel, discord.channel.TextChannel):
        if ctx.author.guild_permissions.administrator:
            channel = ctx.channel
            try:
                if link.startswith("http://") or link.startswith("https://"):
                    response = requests.get(link)
                    if response.status_code == 200:
                        content = response.text
                        message = await channel.fetch_message(message_id)
                        await message.edit(content=content)
                        await ctx.send("Message edited successfully.", ephemeral=True)
                        logging.info(
                            f"message {message_id} edited by {ctx.author.name}"
                        )
                    else:
                        await ctx.send(
                            "Failed to fetch the content from the provided link.",
                            ephemeral=True,
                        )
                else:
                    message = await channel.fetch_message(message_id)
                    await message.edit(content=link)
                    await ctx.send("Message edited successfully.", ephemeral=True)
                    logging.info(f"message {message_id} edited by {ctx.author.name}")
            except Exception as e:
                await ctx.send(f"An error occurred: {e}", ephemeral=True)
                logging.warning(f"error occurred: {e}")
        else:
            await ctx.send(
                "You don't have permissions to edit the message.", ephemeral=True
            )


@bot.hybrid_command()
async def sendattachment(ctx, link, extension):
    if isinstance(ctx.channel, discord.channel.TextChannel):
        if ctx.author.guild_permissions.administrator:
            channel = ctx.channel
            try:
                if link.startswith("http://") or link.startswith("https://"):
                    async with aiohttp.ClientSession() as session:
                        async with session.get(link) as resp:
                            if resp.status == 200:
                                data = io.BytesIO(await resp.read())
                                await channel.send(
                                    file=discord.File(data, "attachment." + extension)
                                )
                                await ctx.send("attachment sent successfully.", ephemeral=True)
                                logging.info(f"attachment sent by {ctx.author.name}")
                            else:
                                await ctx.send(
                                    "Failed to fetch the content from the provided link.",
                                    ephemeral=True,
                                )
                else:
                    await ctx.send("Invalid link.", ephemeral=True)
            except Exception as e:
                await ctx.send(f"An error occurred: {e}", ephemeral=True)
                logging.warning(f"error occurred: {e}")
        else:
            await ctx.send(
                "You don't have permissions to send the attachment.", ephemeral=True
            )


@bot.command()
async def flag(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        logging.info(f"flag called by {ctx.author.name}")
        await ctx.send(f"hi! here's your flag: `{FLAG}`", ephemeral=True)


bot.run(TOKEN)
