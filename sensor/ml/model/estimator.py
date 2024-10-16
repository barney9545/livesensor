from sensor.logger import logging
from sensor.exception import SensorException
import os,sys
from sensor.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME

class TargetValueMapping:
    def __init__(self):
        self.neg : int = 0
        self.pos : int = 1
    
    def to_dict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        return {v:k for k,v in self.to_dict().items()}
    
class SensorModel:
    def __init__(self, processor: object, model: object):
        try:
            self.processor = processor
            self.model = model
        except Exception as e:
            raise e
        
    def predict(self, X):
        try:
            x_transformed = self.processor.transform(X)
            y_pred = self.model.predict(x_transformed)
            logging.info("Prediction done successfully")
            return y_pred
        except Exception as e:
            raise e
        
class ModelResolver:
    def __init__(self, model_dir = SAVED_MODEL_DIR ):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise SensorException(e,sys) from e
        
    def get_latest_model_path(self)->str:
        try:
           timestamps = list(map(int, os.listdir(self.model_dir)))
           latest_timestamp = max(timestamps)
           
           latest_model_path = os.path.join(self.model_dir, f"{latest_timestamp}",MODEL_FILE_NAME)
           return latest_model_path
        except Exception as e:
            raise SensorException(e,sys) from e
    
    def check_model_exists(self)->bool:
        try:
            if not os.path.exists(self.model_dir):
                return False    
            
            timestamps = os.listdir(self.model_dir)
            if len(timestamps) == 0:
                return False
            
            if not os.path.exists(self.get_best_model_path()):
                return False
            return True
        except Exception as e:
            raise SensorException(e,sys) from e
        