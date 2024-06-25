import os
import logging
from sensor.exception import SensorException
import pymongo
import pandas as pd
import numpy as np
import json
from sensor.configuration.mongo_db_connection import MongoClient
import sys

class SensorData:

    def __init__(self):
        try:
            self.mongo_client = MongoClient()
        except Exception as e:
            raise SensorException(e, sys)
        
    def save_csv_file(self, file_path, collection_name:str):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            json_record = json.loads(df.T.to_json()).values()
            logging.info(msg='File converted to json successfully')
        except Exception as e:
            raise SensorException(e, sys)

        try:
            collection = self.mongo_client.database[collection_name]
            collection.insert_many(json_record)
            logging.info(msg='Data inserted into database successfully')
            
            return len(json_record)
        except Exception as e:
            raise SensorException(e, sys)
        
    def export_collection_to_df(self, collection_name:str) -> pd.DataFrame:
        try:
            collection = self.mongo_client.database[collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"],axis=1)
                df.replace({'na':np.nan},inplace=True)
            logging.info(msg='Data fetched from database successfully')
            return df
        except Exception as e:
            raise SensorException(e, sys)
            
        
