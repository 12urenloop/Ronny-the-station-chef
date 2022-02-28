from peewee import *

database = SqliteDatabase('ronny.db')


class Base(Model):
    class Meta:
        database = database


class Detection(Base):
    time = TimestampField()
    mac = CharField()


def database_setup() -> None:
    database.create_tables([Detection])


def database_cleanup() -> None:
    database.close()
