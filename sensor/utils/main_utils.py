import logging
from sensor.exception import SensorException
import pandas as pd
import numpy as np
import os
import sys
import yaml
import dill

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            file =  yaml.safe_load(yaml_file)
            logging.info(f"yaml file: {file_path} loaded successfully")
            return file
    except Exception as e:
        raise SensorException(e, sys)
    
def write_yaml_file(file_path:str, content : object, replace : bool = False) -> None:
    
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(path=file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        logging.info('YAML File path created successfully')
        with open(file_path,'w') as file:
            yaml.dump(content,file)
        logging. info('Yaml file created successfully')
    except Exception as e:
        raise SensorException(e,sys)
    
def save_numpy_array_data(file_path: str, array: np.array) ->None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
        
        logging.info('Numpy array data is saved in file successfully')
    
    except Exception as e:
        raise SensorException(e, sys)
    
def load_numpy_array_data(file_path: str) -> np.array:
    try:
        with open(file_path, 'rb') as file_obj:
            array = np.load(file_obj)
            logging.info('Numpy array data is loaded in file successfully')
            return array

    except Exception as e:
        raise SensorException(e, sys)

def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered save_object method of main utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            #dill is used for serialization of complex objects
            dill.dump(obj, file_obj)
        logging.info("Object saved in file successfully")
        
    except Exception as e:
        raise SensorException(e, sys)
    
def load_object(file_path: str ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)
            logging.info("Object loaded in file successfully")
            return obj

    except Exception as e:
        raise SensorException(e, sys) from e    
        


