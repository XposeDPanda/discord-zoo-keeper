import discord
from discord.ext import commands

import datetime
import uuid
from utils import storage
Storage = storage.Storage()


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.name = 'Moderation'

    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation - Available.')

    def isEnabled(ctx):
        if Storage.isEnabled(ctx.guild, 'Moderation') is False:
            raise commands.DisabledCommand()
        else:
            return True


    @commands.command(usage='[member] [reason]')
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.check(isEnabled)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = "No reason specified."
        await member.kick(reason=f'User was kicked by: {ctx.message.author.name} - Reason was: {reason}')

    @commands.command(usage='[member] [reason]')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.check(isEnabled)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reaon = "No reason specified."
        await member.ban(reason=f'User was banned by: {ctx.message.author.name} - Reason was: {reason}')

    @commands.command(usage='[amount]')
    @commands.guild_only()
    @commands.check(isEnabled)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @commands.command(usage='[member] [reason]')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.check(isEnabled)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = "No reason specified."
        mRole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(mRole, reason=f'User was muted by: {ctx.message.author.name} - Reason was: {reason}')

    @commands.command(usage='[member] [reason]')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.check(isEnabled)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = "No reason specified."
        mRole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mRole, reason=f'User was muted by: {ctx.message.author.name} - Reason was: {reason}')

    @commands.command(usage='[member] [reason]')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.check(isEnabled)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = "No reason specified."
        warnID = str(uuid.uuid4().hex)
        wMsg = f'User was warned by: {ctx.message.author.name} - Reason was: {reason}'
        Storage.addWarn(warnID, ctx.guild.id, member, wMsg)

        warnEmbed = discord.Embed()
        warnEmbed.title = "User has been Warned!"
        warnEmbed.description = f"{member.name} {wMsg[4:]}"
        warnEmbed.colour = discord.Colour.red()
        warnEmbed.timestamp = datetime.datetime.now()
        warnEmbed.set_footer(text=f"Warning ID: {warnID}")
        await ctx.channel.send(embed=warnEmbed)
    
    @commands.command(usage='[warnID]')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.check(isEnabled)
    async def removeWarn(self, ctx, *, warnID: str):
        Storage.removeWarn(warnID, ctx.message.guild.id)

    @kick.error
    @ban.error
    @mute.error
    @unmute.error
    async def kickError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Please specify a user when using that command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.channel.send("Could not get user, please mention a user in this server.")
        elif isinstance(error, commands.DisabledCommand):
            await ctx.channel.send("Moderation module is not enabled.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.channel.send("You do not have permissions to use this command.")
        else:
            print(error)

    @purge.error
    async def purgeError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Please specify an amount of messages to remove.")
        elif isinstance(error, commands.DisabledCommand):
            await ctx.channel.send("Moderation module is not enabled.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.channel.send("You do not have permissions to use this command.")
        else:
            print(error)

def setup(client):
    client.add_cog(Moderation(client))