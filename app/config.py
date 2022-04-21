from .models import Database, Analyze
from dotenv import load_dotenv
import os

load_dotenv()

mongodb_connstring = os.environ['MONGODB_CONNSTRING']

db = Database(mongodb_connstring)

analyze = Analyze()
