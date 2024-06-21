import pandas as pd
import json
from sensor.config import mongo_client
from sensor.exception import SensorException
import sys

def dump_csv_to_mongo(file: str, database: str, collection: str) -> None:
    try:
        
        
        df = pd.read_csv(file)
        df.reset_index(drop=True, inplace=True)
        json_file = df.T.to_json()
        # Transpose is used so that each row index is its own key with the value as a dict of record for that row
        # Values is used to get the records without the indices
        json_records = json.loads(json_file).values()

        mongo_client[database][collection].insert_many(json_records)

    except Exception as e:
        raise SensorException(e, sys)
