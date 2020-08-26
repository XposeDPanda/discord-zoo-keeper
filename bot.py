import discord
import utils.openCV

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
        await utils.openCV.image_manipulation(imageURL)

    else:
        ## No attachment found
        return

client.run(bot_token)