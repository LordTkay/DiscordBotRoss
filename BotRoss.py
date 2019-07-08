# External libraries
import logging
import asyncio
import configparser
import os

from discord.ext.commands import Bot

# Local libraries
from Local.Secrets import BOT_TOKEN

# ----------------------------------------------------------------------------------------------------------------------
# Functions


def load_config(path):
    """Loading the config file"""
    config = configparser.ConfigParser()
    if os.path.exists(path):
        logging.info('Configfile {} found.'.format(path))
        config.read(path)
        logging.info('Configfile {} read.'.format(path))
        return config
    else:
        logging.info('Configfile not found at {}. Will be created.'.format(path))
        config['DISCORD'] = {}
        discord = config['DISCORD']
        discord['Bot_Prefix'] = '!'

        config['SERVER'] = {}
        server = config['SERVER']
        server['Backup_Time'] = '10:00'

        with open(path, 'w') as configfile:
            config.write(configfile)
            logging.info('Configfile created at {}.'.format(path))

        return config

# ----------------------------------------------------------------------------------------------------------------------
# Class


class BotRoss(Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix=command_prefix)

    # Bot Events
    async def on_ready(self):
        """This function is called after the bot started."""
        logging.info('Bot client successfully started!')
        logging.info('Bot logged in \'{0.name}\' ({0.id})'.format(bot_ross.user))


# ----------------------------------------------------------------------------------------------------------------------
# Constants

CONFIG_PATH = 'config.ini'

# ----------------------------------------------------------------------------------------------------------------------
# Main

# Setting up the logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

# Loading the config
config = load_config(CONFIG_PATH)
discord_config = config['DISCORD']
server_config = config['SERVER']

# Creating object Bot
bot_ross = BotRoss(command_prefix=discord_config['Bot_Prefix'])
logging.info('Bot object created with prefix: "{}".'.format(discord_config['Bot_Prefix']))

# Starting the bot
bot_ross.run(BOT_TOKEN)

