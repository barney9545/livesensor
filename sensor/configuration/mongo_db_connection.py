from dotenv import load_dotenv
import os
import pymongo
import json
from sensor.constant.env_variable import MONGO_DB_URL_KEY
from sensor.exception import SensorException
import sys
from sensor.constant.database import DATABASE_NAME,COLLECTION_NAME
import logging
import certifi
ca = certifi.where()

load_dotenv()

class MongoClient:
    
    client  = None
    
    def __init__(self,database_name : str = DATABASE_NAME) -> None:
        try:
            self.database_name = database_name
            mongo_db_url = os.getenv(MONGO_DB_URL_KEY)
            if mongo_db_url is None:
                raise SensorException(
                    message = f"Environment variable: {MONGO_DB_URL_KEY} is not set"
                )
            logging.info(msg=f'mongo db url: {mongo_db_url}')
            
            """ if 'localhost' in mongo_db_url:
                self.client = pymongo.MongoClient(mongo_db_url)
            else: """
            self.client = pymongo.MongoClient(mongo_db_url)
            logging.info(msg="mongo db connection created successfully")
            self.database = self.client[self.database_name]
            logging.info(msg="database created successfully")
            
        except Exception as e:
            raise SensorException(e,sys) 
    