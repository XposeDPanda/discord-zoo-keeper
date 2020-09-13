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

from utils.storage import Storage
Storage = Storage()

### Events listeners ###
@client.event
async def on_ready():
    print(f'Logged in as {client.user} --- {client.user.id}')
    print(f'Conntected to: {len(client.guilds)} guilds')


@client.event
async def on_message(message):
    if type(message.channel) is discord.DMChannel:
        return

    if "good bot" in message.content.lower():
        await message.channel.send('Thanks :heart:')

    if "bad bot" in message.content.lower():
        await message.channel.send('I\'m sorry :frowning:')

    if not message.author.bot:
        await client.process_commands(message)




## on guild join ##
@client.event
async def on_guild_join(guild):
    try:
        Storage.add_guild(guild)
    except Exception as err:
        print(err)

@client.command()
async def resetconfig(ctx):
    try:
        Storage.add_guild(ctx.guild)
    except Exception as err:
        print(err)




### Misc/General Commands ###
@client.command()
async def ping(ctx):
    await ctx.channel.send(f'Pong! {round(client.latency * 1000)}ms')




###### Manual Loading/Unloading of Cogs #####
@commands.is_owner()
@client.command()
async def load(ctx, extension: str):
    try:
        client.load_extension(f'cogs.{extension}')
    except(AttributeError, ImportError) as e:
        print(f'{type(e).__name__}: {e}')
        await ctx.channel.send('There was an issue loading that module.')
        return
    await ctx.channel.send(f'{extension} loaded.')


@commands.is_owner()
@client.command()
async def unload(ctx, extension: str):
    try:
        client.unload_extension(f'cogs.{extension}')
    except(AttributeError, ImportError) as e:
        print(f'{type(e).__name__}: {e}')
        await ctx.channel.send('There was an issue unloading that module.')
        return
    await ctx.channel.send(f'{extension} unloaded.')


@commands.is_owner()
@client.command()
async def reload(ctx, extension: str):
    try:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
    except(AttributeError, ImportError) as e:
        print(f'{type(e).__name__}: {e}')
        await ctx.channel.send('There was an issue reloading that module.')
        return
    await ctx.channel.send(f'{extension} reloaded.')


###### Auto Load Cogs and start bot #####
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv("BOT_TOKEN"))