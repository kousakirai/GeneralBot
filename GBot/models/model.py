from mongoengine import (
    Document,
    StringField,
    IntField,
    BooleanField,
    ListField
)


class Level(Document):
    id = IntField(
        required=True,
        primary_key=True
        )
    level = IntField(
        required=True,
        default=1
        )
    exp = IntField(
        required=True,
        default=0
        )


class Guild(Document):
    id = IntField(
        required=True,
        primary_key=True
        )
    prefix = StringField(
        required=False,
        default="g!"
        )
    level = BooleanField(
        default=True
        )
    level_exp = IntField(
        default=6
    )
    level_width = ListField(IntField(
        default=[1,5], max_length=2
    ))
    auth = BooleanField(
        default=False
        )
    authch = IntField(
        required=False,
        default=None
        )
    authrole = IntField(
        required=False,
        default=None
        )


class Auth(Document):
    id = IntField(
        required=True,
        primary_key=True
        )
    password = IntField(
        required=True
        )

class Gban(Document):
    id = IntField(
        required=True,
        primary_key=True
    )
    reason = StringField(
        required=True
    )