import discord
from discord.ext import commands

from utils import storage

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.Storage = storage.Storage()
        self.name = 'Moderation'
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation - Available.')
    
    @commands.command(usage='[member] [reason]')
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if self.Storage.isEnabled(ctx.guild, self.name) is False:
            return
        
        if reason is None:
            reason = "No reason specified."
        
        await member.kick(reason=f'User was kicked by: {ctx.message.author.name} - Reason was: {reason}')
    
    @commands.command(usage='[member] [reason]')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if self.Storage.isEnabled(ctx.guild, self.name) is False:
            return
        
        if reason is None:
            reaon = "No reason specified."
        
        await member.ban(reason=f'User was banned by: {ctx.message.author.name} - Reason was: {reason}')

    @commands.command(usage='[amount]')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        if self.Storage.isEnabled(ctx.guild, self.name) is False:
            return
        await ctx.channel.purge(limit=amount)

    @commands.command(usage='[member] [reason]')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        if self.Storage.isEnabled(ctx.guild, self.name) is False:
            return

        if reason is None:
            reason = "No reason specified."
        
        mRole = discord.utils.get(ctx.guild.roles, name="Muted")
        
        await member.add_roles(mRole, reason=f'User was muted by: {ctx.message.author.name} - Reason was: {reason}')

    @commands.command(usage='[member] [reason]')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        if self.Storage.isEnabled(ctx.guild, self.name) is False:
            return

        if reason is None:
            reason = "No reason specified."

        mRole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mRole, reason=f'User was muted by: {ctx.message.author.name} - Reason was: {reason}')


    @kick.error
    @ban.error
    @mute.error
    @unmute.error
    async def kickError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a user when using that command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Could not get user, please mention a user in this server.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permissions to use this command.")
        else:
            print(error)

    @purge.error
    async def purgeError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify an amount of messages to remove.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permissions to use this command.")
        else:
            print(error)

def setup(client):
    client.add_cog(Moderation(client))