import os,sys
from sensor.constant.training_pipeline import *
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.entity.config_entity import TrainingPipelineConfig,DataingestionConfig,DataValidationConfig
from sensor.entity.artifacts_entity import DataIngestionArtifact,DataValidationArtifact

class TrainingPipeline:
    def __init__(self):
        
        self.training_pipeline_config = TrainingPipelineConfig()
            
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.data_ingestion_cofig = DataingestionConfig(training_pipeline_config=self.training_pipeline_config)
            
            logging.info("Starting data ingestion")
            
            self.data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_cofig)
            
            self.data_ingestion_artifact = self.data_ingestion.initiate_data_ingestion()
            
            logging.info(f"Data ingestion completed and artifact: {self.data_ingestion_artifact}")
            
            return self.data_ingestion_artifact
        
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
            self.data_validation_config = DataValidationConfig( training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data validation")
            self.data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=self.data_validation_config)
            self.data_validation_artifact = self.data_validation.initiate_data_validation()
            logging.info(f"Data validation completed and artifact: {self.data_validation_artifact}")
            return self.data_validation_artifact
        
        except Exception as e:
            raise SensorException(e,sys)
    
    def run_pipeline(self):
        try:
            logging.info(f"Starting training pipeline")
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact: DataValidationArtifact = self.start_data_validation(data_ingestion_artifact)
            logging.info(f"training pipeline completed")
            return data_ingestion_artifact,data_validation_artifact
        except Exception as e:
            raise SensorException(e,sys)
                
       