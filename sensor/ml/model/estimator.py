from sensor.logger import logging
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
        