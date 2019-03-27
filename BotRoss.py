# External Libraries
import logging
import schedule
import threading
import time
import asyncio
from os import path, makedirs
from discord.ext.commands import Bot, has_permissions, MissingPermissions
from discord import Member, Embed, Color, utils
from typing import Union

# Local Libraries
from Local.Secrets import BOT_TOKEN
from Local.PointSystem import PointSystem
from Local import JSONHandler

# ----------------------------------------------------------------------------------------------------------------------

# Constants
BOT_PREFIX = '!'
DATA_PATH = './Data/'
JSON_FILE = DATA_PATH + 'server_table.json'
BACKUP_TIME = '10:00'

# Variables
bot = Bot(command_prefix=BOT_PREFIX)
point_system = PointSystem()

# ----------------------------------------------------------------------------------------------------------------------

# Functions


def start_up(data_path, json_file):
    """This function checks the required files and folder structures."""
    logging.info('Checking existence of directories and files:')
    # Checking Folder "Data", if it doesn't exists it gets created
    if not path.exists(data_path):
        makedirs(data_path)
        logging.info('Folder "{}" was created'.format(path.basename(path.dirname(data_path))))
    else:
        logging.info('Folder "{}" already exists'.format(path.basename(path.dirname(data_path))))

    # Creating the JSON File for user storage, if it doesn't exists
    JSONHandler.create_json(json_file)

    # Reading JSON File
    server_table = JSONHandler.open_json(json_file)

    return server_table


# Bot Functions


@bot.event
async def on_ready():
    """This function is called after the Server started."""
    logging.info('Bot Client successfully started!')
    logging.info('Bot logged in as \'{0.name}\' ({0.id})'.format(bot.user))


# @bot.event
# async def on_message(message):
#     if message.content.startswith('$thumb'):
#         channel = message.channel
#         await channel.send('Send me that \N{THUMBS UP SIGN} reaction, mate')
#
#         def check(reaction, user):
#             return user == message.author and str(reaction.emoji) == '\N{THUMBS UP SIGN}'
#
#         try:
#             reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
#         except asyncio.TimeoutError:
#             await channel.send('\N{THUMBS DOWN SIGN}')
#         else:
#             await channel.send('\N{THUMBS UP SIGN}')

@bot.event
async def on_message(message):
    if len(message.attachments) > 0:
        if 'png' in message.attachments[0].filename:
            # em = utils.get(bot.emojis, name='eyes')
            await message.add_reaction('\N{THUMBS UP SIGN}')


@bot.command(aliases=['p'], pass_context=True)
async def points(context, option, arg1: Union[Member, int] = None, arg2: Union[Member, int] = None):
    """This command is used to add, subtract, set or show points."""
    target_user = context.message.author

    if option in ('add', 'sub', 'set'):
        if target_user.guild_permissions.administrator:
            if arg2 is not None and isinstance(arg2, Member):
                target_user = arg2
            point_system.check_and_create_user(target_user)

            if option == 'add':
                point_system.add_points(target_user.id, arg1)
            elif option == 'sub':
                point_system.subtract_points(target_user.id, arg1)
            elif option == 'set':
                point_system.set_points(target_user.id, arg1)
        else:
            await context.channel.send('You don\'t have the permission for that {}'.format(target_user.mention))

    elif option == 'show':
        if arg1 is not None and isinstance(arg1, Member):
            target_user = arg1
        point_system.check_and_create_user(target_user)
        user = point_system.get_user(target_user.id)
        user_info = Embed(color=Color.dark_red())
        user_info.set_author(name=target_user)
        user_info.add_field(name='Points', value=user['points'])

        await context.channel.send(embed=user_info)


# ----------------------------------------------------------------------------------------------------------------------
# Main

# Setting up the Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

# Creating and setting up a thread, which checks if it is 10:00 to execute the daily backup of json-files
backup_is_running = threading.Event()


def backup_handler():
    while not backup_is_running.is_set():
        schedule.run_pending()
        time.sleep(5)


backup_thread = threading.Thread(target=backup_handler)
backup_thread.start()
schedule.every(1).minutes.do(lambda: JSONHandler.save_json(JSON_FILE, point_system.dictionary))
# schedule.every().day.at(BACKUP_TIME).do(lambda: JSONHandler.save_json(JSON_FILE, server_table))

point_system.dictionary = start_up(DATA_PATH, JSON_FILE)

# Starting the Bot
bot.run(BOT_TOKEN)



