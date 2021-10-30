from mongoengine import (
    Document, StringField, IntField,
    BooleanField
)


class Level(Document):
    id = IntField(required=True, primary_key=True)
    level = IntField(required=True, default=1)
    exp = IntField(required=True, default=0)


class Guild(Document):
    id = IntField(required=True, primary_key=True)
    prefix = StringField(required=False, default="g!")
    level = BooleanField(default=True)
    auth = BooleanField(default=False)
    authch = IntField(required=False, default=None)
    authrole = IntField(required=False, default=None)


class Auth(Document):
    id = IntField(required=True, primary_key=True)
    password = IntField(required=True)
