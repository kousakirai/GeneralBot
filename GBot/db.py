import os
from mongoengine import connect


class DB:
    def start():
        host = 'mongodb+srv://cluster0.bmq8t.mongodb.net/discord'
        print("Mongoengine起動")
        engine = connect(
            db=os.environ['MYSQL_DATABASE'],
            username=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            host=host,
            port=3308
        )

        return engine

    def close(self):
        self.start.close()
        print("Mongoengine終了")
