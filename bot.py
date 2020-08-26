import discord
import utils.title

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user} --- {0.user.id}'.format(client))

@client.event
async def on_message(message):
    if not message.channel.name == "role-request":
        ### Ignores any message outside of this channel
        return

    if message.author.bot:
        return ### Ignores messages from bots.

    if len(message.attachments) > 0:
        ## Attachment found
        imageURL = message.attachments[0].url
        title = await utils.title.get_title(imageURL)
        if title == 'Pirate Legend':
            try:
                role = discord.utils.get(message.guild.roles, name=title)
                await message.author.add_roles(role)
                await message.add_reaction('\U0001f44d')
                return
            except ValueError:
                await message.channel.send('I can see your title is: {0} however I cannot seem to find the correct role to give you, please contact server management.'.format(title))
        else:
            await message.channel.send('Unfortunetly I could not find the Pirate Legend title in your screenshot, please equip the title to your character and try again. \n Title found: {0}'.format(title))
    else:
        ## No attachment found
        return

client.run(bot_token)