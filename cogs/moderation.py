import discord
from discord.ext import commands

from utils import storage

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.Storage = storage.Storage()
        self.name = 'Moderation'
    
    @commands.command(usage='member')
    @commands.guild_only()
    @commands.has_permissions(kick_member)
    @command.bot_has_permissions(kick_member)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if self.Storage.isEnabled(ctx.guild, self.name) is False:
            return
        
        if reason is None:
            reason = "No reason specified."
        
        await member.kick(reason=f'User was kicked by: {ctx.message.author.name} - Reason was: {reason}')
    
    @commands.command(usage='member')
    @commands.guild_only()
    @commands.has_permissions(ban_member)
    @command.bot_has_permissions(ban_member)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if self.Storage.isEnabled(ctx.guild, self.name) is False:
            return
        
        if reason is None:
            reaons = "No reason specified."
        
        await member.ban(reason=f'User was banned by: {ctx.message.author.name} - Reason was: {reason}')


    @kick.error
    @ban.error
    async def kickError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a user when using that command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Could not get user, please mention a user in this server.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permissions to use this command.")
        else:
            print(error)


def setup(client):
    client.add_cog(Moderation(client))