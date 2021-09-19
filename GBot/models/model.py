from mongoengine import (
    Document, StringField, IntField,
    BooleanField, ListField
)


class Level(Document):
    id = IntField(required=True, primary_key=True)
    level = IntField(required=True, default=1)
    exp = IntField(required=True, default=0)

class Guild(Document):
    id = IntField(required=True, primary_key=True)
    prefix = StringField(required=False, default="g!")
    level = BooleanField(default=True)