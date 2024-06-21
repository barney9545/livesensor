from sensor.exception import SensorException
import sys
import os
from sensor.utils import dump_csv_to_mongo

if __name__ == "__main__":

    filename = 'data.csv'
    db = 'APS_DB'
    collection = 'sensor'
    

    try:
        dump_csv_to_mongo(filename, db, collection)
    except Exception as e:
        print(f"An error occurred: {e}")

    # try:
    #     try:
    #         1/0
    #     except Exception as e:
    #         #print(e)
    #         raise SensorException(e,sys)
    # #this raises an exception and call the sensorException
    # #which again raises an exception
    # #to print just the custom error
    # except SensorException as e:
    #     print (e)
        