import discord
from discord.ext import commands
from utils import title, storage
Storage = storage.Storage()

class title_recognition(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Title Recognition - Available.')

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.channel.name == "role-request":
            ### Ignores any message outside of this channel
            return

        if Storage.isEnabled(ctx.guild, 'TitleRecog') == False:
            ### Checks if module is enabled
            return

        if ctx.author.bot:
            return ### Ignores messages from bots.

        if len(ctx.attachments) > 0:
            ## Attachment found
            imageURL = ctx.attachments[0].url
            titleStr = await title.get_title(imageURL)
            if titleStr == 'Pirate Legend':
                try:
                    role = discord.utils.get(ctx.guild.roles, name=titleStr)
                    await ctx.author.add_roles(role)
                    await ctx.add_reaction('\U0001f44d')
                    return
                except ValueError:
                    await ctx.channel.send(f'I can see your title is: {titleStr} however I cannot seem to find the correct role to give you, please contact server management.')
            else:
                await ctx.channel.send(f'Unfortunetly I could not find the Pirate Legend title in your screenshot, please equip the title to your character and try again. \n Title found: {titleStr}')
        else:
            ## No attachment found
            return
    

def setup(client):
    client.add_cog(title_recognition(client))