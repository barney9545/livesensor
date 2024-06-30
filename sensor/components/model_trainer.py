import os,sys
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import save_numpy_array_data, load_numpy_array_data, save_object, load_object
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.entity.artifacts_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from sensor.ml.metric.classification_metric import get_classification_metric
from sensor.ml.model.estimator import SensorModel

import pandas as pd
import numpy as np
from xgboost import XGBClassifier

class ModelTrainer:

    def __init__(self, model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            logging.info(f"{'>>' * 20}Model Trainer log started.{'<<' * 20}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys) from e

    def hyperparameter_tuning(self):
        pass
    
    def train_model(self, X, y):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(X, y)
            return xgb_clf
        except Exception as e:
            raise SensorException(e, sys) from e
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            logging.info("Loaded train and test array.")
            
            x_train,y_train,x_test,y_test = train_arr[:,:-1],train_arr[:,-1],test_arr[:,:-1],test_arr[:,-1]
            logging.info("x_train,y_train,x_test,y_test split completed")
            
            model= self.train_model(x_train,y_train)
            logging.info("Model trained successfully.")

            y_train_pred = model.predict(x_train)
            logging.info("y_train_pred created successfully.")
            
            train_classification_metric = get_classification_metric(y_train,y_train_pred)
            
            if train_classification_metric.f1_score <= self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {train_classification_metric}")
            logging.info("Model performance is above the expected accuracy.")
            
            y_test_pred = model.predict(x_test) 
            logging.info("y_test_pred created successfully.")
            
            test_classification_metric = get_classification_metric(y_test,y_test_pred)
            
            diff = abs(train_classification_metric.f1_score - test_classification_metric.f1_score)
            
            if diff > self.model_trainer_config.underfitting_overfitting_threshold:
                raise Exception(f"Model is not good as the difference between train and test f1 score is: {diff}: model actual score: {test_classification_metric}")
            logging.info("Underfitting or overfitting check passed.")
            
            processor = load_object(self.data_transformation_artifact.transformed_object_file_path)
            
            model_dir = os.path.dirname(self.model_trainer_config.model_trainer_trained_model_file_path)
            os.makedirs(model_dir,exist_ok=True)
            
            sensor_model = SensorModel(processor=processor, model=model)
            
            save_object(obj=sensor_model, file_path=self.model_trainer_config.model_trainer_trained_model_file_path)
            logging.info(f"Model saved successfully at {self.model_trainer_config.model_trainer_trained_model_file_path}")
            
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.model_trainer_trained_model_file_path,
                train_metric_artifact=train_classification_metric.f1_score,
                test_metric_artifact=test_classification_metric.f1_score,
                is_trained=True,
                message="Model Trained successfully",
                error_message=None
            )
            
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise SensorException(e, sys) from e
            