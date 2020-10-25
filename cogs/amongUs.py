import discord
from discord.ext import commands

from utils import storage
Storage = storage.Storage()

currentGames = {}
keys_to_remove = []

class AmongUs(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Among Us - Available.')
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if Storage.isEnabled(ctx.guild, 'TitleRecog') == False:
            ### Checks if module is enabled
            return

        try:
            for key, game in currentGames.items():
                if before.channel is not after.channel:
                    if before.channel and before.channel.id == game['voiceID']:
                        if member.id in game['players']:
                            await self.removePlayer(key, game, member)

                    if after.channel and after.channel.id == game['voiceID']:
                        if member.id not in game['players']:
                            await self.addPlayer(game, member)
            if keys_to_remove:
                await self.deleteGame()
        except Exception as err:
            print(err)

    async def addPlayer(self, game, member):
        textChannel = self.client.get_channel(game['textID'])
        game['players'].append(member.id)
        overwrite = textChannel.overwrites_for(member)
        overwrite.read_messages = True
        overwrite.send_messages = True
        await textChannel.set_permissions(member, overwrite=overwrite)

    async def removePlayer(self, key, game, member):
        textChannel = self.client.get_channel(game['textID'])
        voiceChannel = self.client.get_channel(game['voiceID'])
        game['players'].remove(member.id)
        overwrite = textChannel.overwrites_for(member)
        overwrite.send_messages = False
        overwrite.read_messages = False
        await textChannel.set_permissions(member, overwrite=overwrite)
        if not game['players']:
            await textChannel.delete()
            await voiceChannel.delete()
            keys_to_remove.append(key)
    
    async def deleteGame(self):
            for key in keys_to_remove:
                del currentGames[key]

    @commands.command(usage=None)
    @commands.guild_only()
    async def create(self, ctx):
        if Storage.isEnabled(ctx.guild, 'TitleRecog') == False:
            ### Checks if module is enabled
            return

        try:
            if any([ctx.message.author.id in game['players'] for game in currentGames.values()]):
                await ctx.send("You're already part of a game, please leave your current game before making a new one.")
            else:
                #Get category and text channel overwrites to make private channel
                category = discord.utils.get(ctx.guild.categories, name="Game Channels")
                textOverwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
                }

                # create game object and add to current games
                game = {}
                voice = await ctx.guild.create_voice_channel(name=f'Game{len(currentGames)+1} Voice', user_limit=10, category=category)
                text = await ctx.guild.create_text_channel(name=f'Game{len(currentGames)+1} Text', category=category, overwrites=textOverwrites)
                game['voiceID'] = voice.id
                game['textID'] = text.id
                game['players'] = []
                currentGames[f'{len(currentGames)}'] = game
                await self.addPlayer(game, ctx.message.author)

                await ctx.send(f'Hey Everyone!! {ctx.message.author.mention} just started a game! Come and <@&764151254976036874>!')
        except Exception as err:
            await ctx.send(err)
    
    @commands.command(usage=None)
    @commands.guild_only()
    async def leave(self, ctx):
        if Storage.isEnabled(ctx.guild, 'TitleRecog') == False:
            ### Checks if module is enabled
            return
            
        if any([ctx.message.author.id in game['players'] for key, game in currentGames.items()]):
            await self.removePlayer(key, game, ctx.message.author)
            if keys_to_remove:
                await self.deleteGame()

def setup(client):
    client.add_cog(AmongUs(client))
