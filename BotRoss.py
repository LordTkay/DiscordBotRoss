import Secrets

import discord
from discord.ext.commands import Bot

BOT_PREFIX = '!'
BOT_TOKEN = Secrets.BOT_TOKEN

client = Bot(command_prefix=BOT_PREFIX)


# Function will be called after a successful start of the Bot
@client.event
async def on_ready():
    print('Started Successfully')
    print('Logged in as \'{0.name}\' ({0.id})'.format(client.user))


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     await client.send_message(message.channel, 'Moin Moin')


@client.command(pass_context=True)
async def speak(ctx, arg):
    # print(ctx.message)
    await client.send_message(ctx.message.channel, arg)

client.run(BOT_TOKEN)
