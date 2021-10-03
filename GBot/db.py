import os
from mongoengine import connect


class DB:
    def engine():
        print("Mongoengine起動")
        engine = connect(db=os.environ['MYSQL_DATABASE'],
                              username=os.environ['MYSQL_USER'],
                              password=os.environ['MYSQL_PASSWORD'],
                              host='mongodb+srv://cluster0.bmq8t.mongodb.net/discord',
                              port=3308
                              )

        return engine

    def shutdown(self, *args, **kwargs):
        self.engine.close()
        print("Mongoengine終了")
