from datetime import datetime as dt
import os
from sensor.constant import training_pipeline
from sensor.exception import SensorException
import sys

class TrainingPipelineConfig:
    
    def __init__(self,timestamp=dt.now()):
        try:
            timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
            
            self.pipeline_name: str = training_pipeline.PIPELINE_NAME
            self.timestamp : str = timestamp
            self.artifact_dir: str = os.path.join(training_pipeline.ARTIFACT_DIR, timestamp)
            
        except Exception as e:
            raise SensorException(e,sys)
        
class DataingestionConfig:
    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)
            self.feature_store_dir: str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME)
            self.training_file_path: str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE)
            self.testing_file_path: str = os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TEST_FILE)
            self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
            self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
            
        except Exception as e:
            raise SensorException(e,sys)
        
class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
            self.valid_data_dir: str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
            self.invalid_data_dir: str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)
            self.valid_train_file_path: str = os.path.join(self.valid_data_dir,training_pipeline.TRAIN_FILE)
            self.valid_test_file_path: str = os.path.join(self.valid_data_dir,training_pipeline.TEST_FILE)
            self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir,training_pipeline.TRAIN_FILE)
            self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir,training_pipeline.TEST_FILE)
            self.drift_report_file_path: str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_DIRFT_REPORT_DIR,training_pipeline.DATA_VALIDATION_DIRFT_REPORT_FILE_NAME)
        except Exception as e:
            raise SensorException(e,sys)

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
            self.transformed_train_file_path: str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,training_pipeline.TRAIN_FILE.replace(".csv",".npy"))
            self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,training_pipeline.TEST_FILE.replace(".csv",".npy"))
            self.transformed_object_file_path: str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,training_pipeline.PREPROCSSING_OBJECT_FILE_NAME)
        
        except Exception as e:
            raise SensorException(e,sys)

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME)
            self.model_trainer_trained_model_dir: str = os.path.join(self.model_trainer_dir,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR_NAME) # model_trainer_trained_model_dir
            self.model_trainer_trained_model_file_path: str = os.path.join(self.model_trainer_trained_model_dir,training_pipeline.MODEL_FILE_NAME)
            self.expected_score: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
            self.underfitting_overfitting_threshold: float = training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD
        except Exception as e:
            raise SensorException(e,sys) from e
        
class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_evaluation_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_EVALUATION_DIR_NAME)
            self.mode_evaluation_report_file_path = os.path.join(self.model_evaluation_dir, training_pipeline.MODEL_EVALUATION_REPORT_FILE_NAME)
            self.model_evaluation_threshold = training_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE
        except Exception as e:
            raise SensorException(e,sys) from e
        
class ModelPusherConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_pusher_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_PUSHER_DIR_NAME)
            self.model_file_path = os.path.join(self.model_pusher_dir, training_pipeline.MODEL_FILE_NAME) 
            
            #saved models
            timesstamp = dt.now().strftime("%Y%m%d%H%M%S")
            self.saved_model_path = os.path.join(training_pipeline.SAVED_MODEL_DIR, f"{timesstamp}",training_pipeline.MODEL_FILE_NAME)
            
        except Exception as e:
            raise SensorException(e,sys) from e