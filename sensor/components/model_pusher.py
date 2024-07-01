import os,sys
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import save_numpy_array_data, load_numpy_array_data, save_object, load_object
from sensor.entity.config_entity import ModelEvaluationConfig, ModelPusherConfig
from sensor.entity.artifacts_entity import  ClassificationMetricArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from sensor.ml.metric.classification_metric import get_classification_metric
from sensor.ml.model.estimator import SensorModel, TargetValueMapping , ModelResolver
import pandas as pd
from sensor.constant.training_pipeline import TARGET_COLUMN
import shutil #used to copy foles from source to destination

class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig,
                 model_evaluation_artifact: ModelEvaluationArtifact
                 ):
        try:
            logging.info(f"{'>>'*20}Model Pusher log started.{'<<'*20}")
            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact
            
        except Exception as e:
            raise SensorException(e,sys) from e
    
    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            trained_model_file_path = self.model_evaluation_artifact.trained_model_path
            
            model_file_path = self.model_pusher_config.model_file_path
            
            os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
            
            shutil.copy(src= trained_model_file_path, dst= model_file_path)
            logging.info(f"Trained model {trained_model_file_path} copied successfully in {model_file_path}")
            
            #saved model file path
            saved_model_file_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_file_path), exist_ok=True)
            shutil.copy(src= trained_model_file_path, dst= saved_model_file_path)
            logging.info(f"Trained model {trained_model_file_path} copied successfully in {saved_model_file_path}")
            
            #prepare artifact
            model_pusher_artifact = ModelPusherArtifact(
                saved_model_path= saved_model_file_path,
                model_file_path= model_file_path,
                message="Model pushed successfully",
                error_message=None
            )
            logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e,sys) from e