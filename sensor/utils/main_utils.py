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
        


