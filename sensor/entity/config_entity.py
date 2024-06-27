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
            