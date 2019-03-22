# Local Libraries
from Local.Secrets import BOT_TOKEN
from Local.PointSystem import PointSystem

# External Libraries
import json
import os
import schedule
import threading
import time
import discord
from discord.ext.commands import Bot
from discord import Member


BOT_PREFIX = '!'
DATA_PATH = './Data/'
POINTS_FILE = DATA_PATH + 'points.json'

client = Bot(command_prefix=BOT_PREFIX)
point_system = PointSystem()


# Function will be called after a successful start of the Bot
@client.event
async def on_ready():
    print('Sever successfully started!')
    print('Bot logged in as \'{0.name}\' ({0.id})'.format(client.user))


@client.command(pass_context=True)
async def points(context, option, amount_points=0, target_user: Member = None):
    if target_user is None:
        target_user = context.message.author

    print('{} {}'.format(option, amount_points))
    if option == 'add':
        point_system.add(target_user.id, amount_points)
    elif option == 'sub':
        point_system.subtract(target_user.id, amount_points)
    elif option == 'set':
        point_system.set(target_user.id, amount_points)
    elif option == 'show':
        user = point_system.get_user(target_user.id)
        user_info = discord.Embed(color=discord.Color.dark_red())
        user_info.set_author(name=target_user)
        user_info.add_field(name='Points', value=user['points'])

        await client.send_message(context.message.channel, embed=user_info)


print('\nChecking directories and files:')
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)
    print('{} was created'.format(os.path.abspath(DATA_PATH)))
else:
    print('{} exists'.format(os.path.abspath(DATA_PATH)))

point_system.create_json(POINTS_FILE)

print('\nReading files:')
point_system.open_json(POINTS_FILE)
print('Finished loading files.')


backup_run = threading.Event()


def backup_json():
    while not backup_run.is_set():
        schedule.run_pending()
        time.sleep(5)


backup_thread = threading.Thread(target=backup_json)
backup_thread.start()
# schedule.every(1).minute.do(lambda: point_system.save_json(POINTS_FILE))
schedule.every().day.at("10:00").do(lambda: point_system.save_json(POINTS_FILE))

client.run(BOT_TOKEN)

# Scraps:

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
