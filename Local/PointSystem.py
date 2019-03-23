# External Libraries
import os
import logging
from discord import Member

# ----------------------------------------------------------------------------------------------------------------------

# Constants
BASE_JSON = {'users': []}
BASE_USER_JSON = {'id': 0, 'name': '', 'points': 0}

# ----------------------------------------------------------------------------------------------------------------------


class PointSystem:

    def __init__(self):
        self.dictionary = []

    def enter_branch(self, branch):
        """Check if the branch is in the dictionary. If it's true, the branch will be returned."""
        if branch in self.dictionary:
            return self.dictionary[branch]
        else:
            logging.WARNING('JSON doesn\'t contain branch "{}"! Can\'t fulfill operation.'.format(branch))

    def check_and_create_user(self, member: Member):
        """Checking if the user exists, if appending him."""
        users = self.enter_branch('users')
        for user in users:
            if user['id'] == member.id:
                return

        new_user = BASE_USER_JSON
        new_user['id'] = member.id
        new_user['name'] = member.name
        users.append(new_user)
        logging.info('User "{}({})" was created'.format(new_user['name'], new_user['id']))

    def get_user(self, user_id):
        """Search for the user id inside of the dictionary and returns it."""
        users = self.enter_branch('users')
        for user in users:
            if user['id'] == user_id:
                return user

    def add_points(self, user_id, value):
        """Adding an amount of points to the passed user."""
        user = self.get_user(user_id)
        user['points'] += value
        if user['points'] < 0:
            user['points'] = 0
        logging.info('User "{}({}) received {} points: {}'.format(user['name'], user['id'], value, user['points']))

    def subtract_points(self, user_id, value):
        """Subtracting an amount of points to the passed user."""
        user = self.get_user(user_id)
        user['points'] -= value
        if user['points'] < 0:
            user['points'] = 0
        logging.info('User "{}({}) lost {} points: {}'.format(user['name'], user['id'], value, user['points']))

    def set_points(self, user_id, value):
        """Setting an amount of points to the passed user."""
        user = self.get_user(user_id)
        user['points'] = value
        if user['points'] < 0:
            user['points'] = 0
        logging.info('User "{}({}) was set to {} points'.format(user['name'], user['id'], user['points']))

