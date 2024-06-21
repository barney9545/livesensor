from dataclasses import dataclass
import os
import pymongo
import pymongo.mongo_client

@dataclass
class Enviroment_variable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")

env_var = Enviroment_variable()

mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
