# External Libraries
import json
import os
import logging

# Local Libraries
from .PointSystem import BASE_JSON

# ----------------------------------------------------------------------------------------------------------------------


def create_json(file_path):
    """Check if the file exists, if not it will be created."""
    absolute_path = os.path.abspath(file_path)
    file_name = os.path.basename(absolute_path)

    try:
        open(absolute_path, 'x')
    except FileExistsError:
        logging.info('JSON "{}" already exists'.format(file_name))
        return

    with open(absolute_path, 'w') as file:
        json.dump(BASE_JSON, file)
    logging.info('JSON "{}" was created'.format(file_name))


def open_json(file_path):
    """Try to open an JSON file which will be loaded as dictionary if it exists."""
    absolute_path = os.path.abspath(file_path)
    file_name = os.path.basename(absolute_path)
    json_dictionary = None

    try:
        with open(absolute_path) as file:
            json_dictionary = json.load(file)
            logging.info('JSON file "{}" has been loaded'.format(file_name))
    except FileNotFoundError as error:
        logging.error(error)

    return json_dictionary


def save_json(file_path, dictionary):
    """Saving the current state of an dictionary into a JSON file."""
    absolute_path = os.path.abspath(file_path)
    file_name = os.path.basename(absolute_path)
    temp_path = absolute_path + '.tmp'

    with open(temp_path, 'w') as file:
        json.dump(dictionary, file)
    os.remove(absolute_path)
    os.rename(temp_path, absolute_path)
    logging.info('{} was successfully saved.'.format(file_name))
