# Discord bot
# Originally intended to work as an image recognition bot for the Pirate Legend role request channel in several Sea of Thieves discord guilds.
# Now an all purpose discord bot with several toggleable modules.
# Written by The Panda#9999
#Any queries feel free to message me on discord.

import os
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands
client = commands.Bot(command_prefix="!", help_command=None, case_insensitive=True)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} --- {client.user.id}')
    print(f'Conntected to: {len(client.guilds)} guilds')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def ping(ctx):
    await ctx.channel.send(f'Pong! {round(client.latency * 1000)}ms')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(os.getenv("BOT_TOKEN"))