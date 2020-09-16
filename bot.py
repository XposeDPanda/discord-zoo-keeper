# Discord bot
# Originally intended to work as an image recognition bot for the Pirate Legend role request channel in several Sea of Thieves discord guilds.
# Now an all purpose discord bot with several toggleable modules.
# Written by The Panda#9999
#Any queries feel free to message me on discord.

import os
import time, datetime
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands
client = commands.Bot(command_prefix="!", help_command=None, case_insensitive=True)

startTime = time.time()

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



## on guild specific stuff ##


# DEV COMMAND to mimic joining/leaving of guild





### Misc/General Commands ###
@client.command(usage=None)
async def ping(ctx):
    await ctx.channel.send(f'🏓Pong! {round(client.latency * 1000)}ms')

@client.command(usage=None)
async def uptime(ctx):
    curTime = time.time()
    timeDif = int(round(curTime - startTime))
    try:
        await ctx.channel.send(f'The bot has been up for: {datetime.timedelta(seconds=timeDif)}')
    except Exception as e:
        await ctx.channel.send(e)

@client.command(usage='[module]')
async def help(ctx,*cogName):
    try:
        helpEmbed = discord.Embed(title="Help.",
                                color=discord.Color(0x049bff),
                                description=f'For more information about a specific module try: !help [module] (Case sensitive)')
        if len(cogName) > 1:
            helpEmbed = discord.Embed(title="Error!",
                                    color=discord.Color.red(),
                                    description='Please only enter one module.')
            await ctx.channel.send(embed=helpEmbed)
        if not cogName:
            cogList = ''
            for cog in client.cogs:
                if len(client.get_cog(cog).get_commands()) > 0:
                    cogList += f'{cog} \n'
            helpEmbed.add_field(name='Modules', value=cogList, inline=False)
            cmdList = ''
            for cmd in client.walk_commands():
                if not cmd.usage:
                    usage = f'{client.command_prefix}{cmd.name}'
                else:
                    usage = f'{client.command_prefix}{cmd.name} {cmd.usage}'
                if not cmd.hidden and not cmd.cog_name:
                    cmdList += f'{cmd.name} - {usage} \n'
            helpEmbed.add_field(name='General Commands', value=cmdList, inline=False)
            await ctx.channel.send(embed=helpEmbed)
        else:
            cmdList = ''
            if len(client.get_cog(cogName[0]).get_commands()) > 0:
                for cmd in client.get_cog(cogName[0]).get_commands():
                    if not cmd.usage:
                        usage = f'{client.command_prefix}{cmd.name}'
                    else:
                        usage = f'{client.command_prefix}{cmd.name} {cmd.usage}'
                    if not cmd.hidden:
                        cmdList += f'{cmd.name} - {usage} \n'
            else:
                cmdList = f'This module does not have any discord commands'
            helpEmbed.add_field(name=f'{cogName[0]} Module', value=cmdList, inline=False)
            await ctx.channel.send(embed=helpEmbed)
    except Exception as e:
        await ctx.channel.send(e)


###### Manual Loading/Unloading of Cogs #####
@commands.is_owner()
@client.command(hidden=True)
async def load(ctx, extension: str):
    try:
        client.load_extension(f'cogs.{extension}')
    except(AttributeError, ImportError) as e:
        print(f'{type(e).__name__}: {e}')
        await ctx.channel.send('There was an issue loading that module.')
        return
    await ctx.channel.send(f'{extension} loaded.')


@commands.is_owner()
@client.command(hidden=True)
async def unload(ctx, extension: str):
    try:
        client.unload_extension(f'cogs.{extension}')
    except(AttributeError, ImportError) as e:
        print(f'{type(e).__name__}: {e}')
        await ctx.channel.send('There was an issue unloading that module.')
        return
    await ctx.channel.send(f'{extension} unloaded.')


@commands.is_owner()
@client.command(hidden=True)
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