from config import *
from peewee import *

db = SqliteDatabase(DATA_BASE["name"])


class Site(Model):

    name = TextField()

    class Meta:
        database = db


class Data(Model):
    site_id = IntegerField()
    email = TextField()
    fullname = TextField()
    phone = TextField()

    class Meta:
        database = db


class Course(Model):
    site_id = IntegerField()
    name = TextField()

    class Meta:
        database = db


class Offer(Model):
    course_id = IntegerField()
    duration_hours = IntegerField()
    duration_days = IntegerField()
    price = IntegerField()

    class Meta:
        database = db


class Museum(Model):
    site_id = IntegerField()
    name = TextField()
    email = TextField()

    class Meta:
        database = db


class Employee(Model):
    museum_id = IntegerField()
    job_title = TextField()
    fullname = TextField()

    class Meta:
        database = db


db.create_tables([Site, Data, Course, Offer, Museum, Employee])
