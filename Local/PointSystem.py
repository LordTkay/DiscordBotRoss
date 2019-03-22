import json
import os

BASE_JSON = {
    'users': []
}


class PointSystem:
    def __init__(self):
        self.point_table = []

    def open_json(self, file_path):
        full_path = os.path.abspath(file_path)

        try:
            with open(file_path) as points_json:
                self.point_table = json.load(points_json)
                print('Loaded {}'.format(full_path))
        except json.decoder.JSONDecodeError:
            print('File has no JSON format or is empty: {}'.format(full_path))

    def save_json(self, file_path):
        full_path = os.path.abspath(file_path)
        tmp_name = file_path + '.bak'

        with open(tmp_name, 'w') as points_json:
            json.dump(self.point_table, points_json)
        os.remove(file_path)
        os.rename(tmp_name, file_path)
        print('Backup created')

    def check_user(self, user_id):
        if 'users' in self.point_table:
            users = self.point_table['users']

            if not any(user['id'] == user_id for user in users):
                users.append({'id': user_id, 'points': 0})

    def get_user(self, user_id):
        self.check_user(user_id)
        for user in self.point_table['users']:
            if user['id'] == user_id:
                return user

    def add(self, user_id, points):
        user = self.get_user(user_id)
        user['points'] += points

    def subtract(self, user_id, points):
        user = self.get_user(user_id)
        user['points'] -= points

    def set(self, user_id, points):
        user = self.get_user(user_id)
        user['points'] = points

    @staticmethod
    def create_json(file_path):
        full_path = os.path.abspath(file_path)

        try:
            open(file_path, 'x')
            with open(file_path, 'w') as points_json:
                json.dump(BASE_JSON, points_json)
            print('{} was created'.format(full_path))
        except FileExistsError:
            print('{} exists'.format(full_path))