import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class Administration(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Administration - Available.')

    @commands.command(usage="[member]")
    @commands.guild_only()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
        except Exception as e:
            await ctx.send(e)

    @commands.command(usage="[member]")
    @commands.guild_only()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
        except Exception as e:
            await ctx.send(e)
    
    @commands.command(usage="[member ID]")
    @commands.guild_only()
    @has_permissions(ban_members=True)
    async def unban(self, ctx, member: int, *, reason=None):
        try:
            user = discord.Object(member)
            await ctx.guild.unban(user=user,reason=reason)
        except Exception as e:
            await ctx.send(e)


    @commands.command(usage="[user]")
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        mRole = discord.utils.get(ctx.guild.roles, name="Muted")

        if not mRole:
            return await ctx.send("No mute role found. Are you sure this if configured correctly?")

            try:
                await member.add_roles(mRole, reason=reason)
            except Exception as e:
                await ctx.send(e)
    
    @commands.command(usage="[user]")
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        mRole = discord.utils.get(ctx.guild.roles, name="Muted")

        if not mRole:
            return await ctx.send("No mute role found. Are you sure this if configured correctly?")

            try:
                await member.remove_roles(mRole, reason=reason)
            except Exception as e:
                await ctx.send(e)
    
    @commands.command(usage="[amount]")
    @commands.guild_only()
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, amount):
        try:
            await ctx.channel.purge(limit=amount)
            await ctx.message.delete()
        except Exception as e:
            await ctx.send(e)
    
    @commands.command(usage="[member]")
    @commands.guild_only()
    @has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, name=None):
        try:
            await member.edit(nick=name)
        except Exception as e:
            await ctx.send(e)



def setup(client):
    client.add_cog(Administration(client))