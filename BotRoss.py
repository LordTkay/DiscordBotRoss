# Local Libraries
from Local.Secrets import BOT_TOKEN

# External Libraries
import json
import os
from discord.ext.commands import Bot

BOT_PREFIX = '!'
DATA_PATH = './Data/'
POINTS_FILE = DATA_PATH + 'points.json'

client = Bot(command_prefix=BOT_PREFIX)
point_table = []


# Function will be called after a successful start of the Bot
@client.event
async def on_ready():

    print('Sever successfully started!')
    print('Bot logged in as \'{0.name}\' ({0.id})'.format(client.user))

    print('\nChecking directories and files:')
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        print('{} was created'.format(os.path.abspath(DATA_PATH)))
    else:
        print('{} exists'.format(os.path.abspath(DATA_PATH)))

    try:
        open(POINTS_FILE, 'x')
        print('{} was created'.format(os.path.abspath(POINTS_FILE)))
    except FileExistsError:
        print('{} exists'.format(os.path.abspath(POINTS_FILE)))

    print('\nReading files:')
    try:
        with open(POINTS_FILE) as points_json:
            point_table = json.load(points_json)
            print('Loaded {}'.format(os.path.abspath(POINTS_FILE)))
    except json.decoder.JSONDecodeError:
        print('File has no JSON format or is empty: {}'.format(os.path.abspath(POINTS_FILE)))

    print('Finished loading files.')
    print('\n{0.name} ready to Work!'.format(client.user))


async def points(context, method, amount_points=0):
    author = context.message.author
    if method == 'add':
        pass
    elif method == 'sub':
        pass
    elif method == 'set':
        pass

client.run(BOT_TOKEN)

#
# @client.command(pass_context=True)
# async def points(context, method, points=0):
#     # print(context.message.author.id)
#     author = context.message.author
#     print(author.id)
#     print(method)
#     if method == 'add':
#         for entry in points_table:
#             print(entry['id'])
#             if entry['id'] == author.id:
#                 entry['points'] += points
#                 print(entry['points'])
#                 await client.send_message(context.message.channel, entry['points'])
#     elif method == 'show':
#         for entry in points_table:
#             if entry['id'] == author.id:
#                 print(entry['points'])
#                 await client.send_message(context.message.channel, entry['points'])
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     await client.send_message(message.channel, 'Moin Moin')

# @client.command(pass_context=True)
# async def speak(ctx, *arg):
#     # print(ctx.message)
#     await client.send_message(ctx.message.channel, arg)