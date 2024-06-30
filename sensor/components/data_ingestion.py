import os
import sys
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataingestionConfig,TrainingPipelineConfig
from sensor.entity.artifacts_entity import DataIngestionArtifact
import pandas as pd
import numpy as np
from sensor.data_access.sensor_data import SensorData
from sklearn.model_selection import train_test_split
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.utils.main_utils import read_yaml_file
class DataIngestion:
    
    def __init__(self,data_ingestion_config:DataingestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e,sys)
    
    def export_data_into_feature_store(self) -> pd.DataFrame:
        """
        Export data into a feature store.

        Returns:
        pd.DataFrame: The dataframe containing the exported data.
        """
        try:
           logging.info("Exporting data into feature store")
           sensor_data = SensorData()
           dataframe = sensor_data.export_collection_to_df(collection_name=self.data_ingestion_config.collection_name)
    
           dataframe.drop(columns=self._schema_config["drop_columns"],inplace=True,axis=1)
           
           feature_store_file_path = self.data_ingestion_config.feature_store_dir
           
           dir_path = os.path.dirname(feature_store_file_path)
           os.makedirs(dir_path,exist_ok=True)
           
           dataframe.to_csv(feature_store_file_path,index=False,header=True)
           
           logging.info("Exported data into feature store")
           return dataframe
       
        except Exception as e:
            raise SensorException(e,sys)
        
    def split_data_as_train_test(self,dataframe:pd.DataFrame) -> None:

           try:
               logging.info("Splitting data into train and test set")
               train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=32)
               logging.info("Performed train test split")
               
               dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
               os.makedirs(dir_path,exist_ok=True)
               logging.info("training path created")
               
               dir_path  = os.path.dirname(self.data_ingestion_config.testing_file_path)
               os.makedirs(dir_path,exist_ok=True)
               logging.info("test path created")
               
               train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
               logging.info("train set created")
               
               test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
               logging.info("test set created")
               
           except Exception as e:
               raise SensorException(e,sys)
           
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        
        try:
            logging.info("Ingestion of data is started")
    
            dataframe = self.export_data_into_feature_store()
            
            self.split_data_as_train_test(dataframe=dataframe)
            
            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
                feature_store_file_path=self.data_ingestion_config.feature_store_dir ,
                is_ingested=True,
                message="Data ingestion completed successfully",
                error_message=None
            )
            
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)