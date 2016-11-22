import sqlite3
from datetime import datetime

class Model:
    def __init__(self):
        self.base = sqlite3.connect('db.db')
        self.cursor = self.base.cursor()

    def save_user(self, username, user_id, tag, operation):
        base = self.base
        base.execute("INSERT INTO instagram_users (username, user_id, tag, date, operation) VALUES ('%s','%s','%s',NULL,'%s')" % (username, user_id, tag, operation))
        base.commit()

    def check_user(self, user_id):
        cursor = self.cursor

        cursor.execute("SELECT * FROM instagram_users WHERE user_id = '%s'" % (user_id))
        row = cursor.fetchone()
        if row != None:
            return True
        else:
            return False

    def get_users_with_operation(self, operation):
        cursor = self.cursor
        cursor.execute("SELECT username, user_id FROM instagram_users WHERE operation = '%s'" % (operation))

        users_info = []
        user_info = cursor.fetchone()

        while user_info is not None:
            users_info.append({'user_id': user_info[1], 'username': user_info[0]})
            user_info = cursor.fetchone()

        return users_info

    def change_operation_status(self, user_id, operation):
        base = self.base
        base.execute("UPDATE instagram_users SET operation = '%s' WHERE user_id = '%s'" % (operation, user_id))
        base.commit()

    def change_date(self, user_id, date=datetime.today()):
        base = self.base
        base.execute("UPDATE instagram_users SET date = '%s' WHERE user_id = '%s'" % (date, user_id))
        base.commit()

    def close(self):
        base = self.base
        base.close()


#db = Model()
#db.save_user('user', '74654', 'dog')
#db.check_user('74655')