import os,sys
from sensor.constant.training_pipeline import *
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.entity.config_entity import TrainingPipelineConfig,DataingestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from sensor.entity.artifacts_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact, ModelTrainerArtifact

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
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact) -> DataTransformationArtifact:
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data transformation")
            self.data_transformation = DataTransformation(data_validation_artifact=self.data_validation_artifact,data_transformation_config=self.data_transformation_config)
            self.data_transformation_artifact = self.data_transformation.initiate_data_transformation()
            logging.info(f"Data transformation completed and artifact: {self.data_transformation_artifact}")
            return self.data_transformation_artifact
        
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting model trainer")
            self.model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config,data_transformation_artifact=self.data_transformation_artifact)
            self.model_trainer_artifact = self.model_trainer.initiate_model_trainer()
            logging.info(f"Model trainer completed and artifact: {self.model_trainer_artifact}")
            return self.model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys) from e
        
    def run_pipeline(self):
        try:
            logging.info(f"Starting training pipeline")
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact: DataValidationArtifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact: DataIngestionArtifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact: ModelTrainerArtifact = self.start_model_trainer(data_transformation_artifact)
            logging.info(f"training pipeline completed")
            
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e,sys)
                
       