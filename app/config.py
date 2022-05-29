import os

from dotenv import load_dotenv

from app.models.database import Database
from app.models.parserwrapper import ParserWrapper

load_dotenv()

MONGODB_CONNSTRING = os.environ['MONGODB_CONNSTRING']

db = Database(MONGODB_CONNSTRING)

parser = ParserWrapper()
