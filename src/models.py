import sqlite3
from datetime import datetime

class Model:
    def __init__(self):
        self.base = sqlite3.connect('db.db')
        self.cursor = self.base.cursor()

    def save_user(self, username, user_id, tag):
        base = self.base
        date = datetime.today()
        base.execute("INSERT INTO instagram_users (username, user_id, tag, date) VALUES ('%s','%s','%s','%s')" % (username, user_id, tag, date))
        base.commit()

    def check_user(self, user_id):
        base = self.base
        cursor = self.cursor

        cursor.execute("SELECT * FROM instagram_users WHERE user_id = '%s'" % (user_id))
        row = cursor.fetchone()
        if row != None:
            return True
        else:
            return False

    def close(self):
        base = self.base
        base.close()


#db = Model()
#db.save_user('user', '74654', 'dog')
#db.check_user('74655')