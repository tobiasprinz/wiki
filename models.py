from datetime import datetime
import peewee

db = peewee.SqliteDatabase('wiki.db')

class Page(peewee.Model):
    pagename = peewee.CharField()
    content = peewee.CharField()
    last_modified = peewee.DateTimeField()

    class Meta:
        database = db