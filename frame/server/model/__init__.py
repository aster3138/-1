from peewee import *

db = SqliteDatabase('data.db')

from .user import *
from .account import *
from .task import *
from .proxy import *

db.create_tables([User, Task, Proxy, Account])
