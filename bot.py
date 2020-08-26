TOKEN = "REPLACE TOKEN!"
import discord
import numpy as np
import cv2
import urllib.request

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
        imURL = message.attachments[0].url
        image = await url_to_image(imURL)
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        
    else:
        ## No attachment found
        return

async def url_to_image(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    resp = urllib.request.urlopen(req)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
    return image

client.run(TOKEN)