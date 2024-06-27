from distutils import dir_util
from sensor.exception import SensorException
from sensor.logger import logging
import sys,os
import pandas as pd
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifacts_entity import DataIngestionArtifact,DataValidationArtifact
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.utils.main_utils import read_yaml_file,write_yaml_file
from scipy.stats import ks_2samp #to check for data drifting

class DataValidation:
    
    def __init__(self, data_validation_config:DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation Initiated. {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        
        except Exception as e:
            raise SensorException(e,sys)
        
    def validate_number_of_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            no_of_columns_schema = len(self._schema_config["columns"])
            no_of_columns_dataframe = len(dataframe.columns)
            logging.info(f"Number of columns in schema: {no_of_columns_schema}")
            logging.info(f"Number of columns in dataframe: {no_of_columns_dataframe}")
            
            if no_of_columns_schema == no_of_columns_dataframe:
                logging.info("Number of columns in schema and dataframe matches.")
                return True
            else:
                return False
        except Exception as e:
            raise SensorException(e,sys)
    
    def numerical_column_exist(self, dataframe:pd.DataFrame) -> bool:
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns
           
            numerical_columns_present = True
            missing_columns = []
            
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_columns_present = False
                    missing_columns.append(num_column)

            logging.info(f"Missing columns: {missing_columns}")
            return numerical_columns_present
        except  Exception as e:
            raise SensorException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e,sys)
    
    def detect_dataset_drift(self,base:pd.DataFrame,current:pd.DataFrame,threshold = 0.01) -> bool:
        try:
            status = False
            #if status is true, drift is detected
            report = dict()

            for column in base.columns:
                d1 = base[column]
                d2 = current[column]
                is_same_dist = ks_2samp(d1,d2)

                if is_same_dist.pvalue >= threshold :
                    drift_in_col = False
                else:
                    drift_in_col = True
                    status = True
                report[column] = {
                    "drift_status":drift_in_col,
                    "p_value":float(is_same_dist.pvalue)
                }
            logging.info(f"Drift Validation completed")
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_name = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_name,exist_ok=True)
            write_yaml_file(drift_report_file_path , report)
            
            logging.info(f"Saved drift report in: {self.data_validation_config.drift_report_file_path}")
            return status
        except Exception as e:
            raise SensorException(e,sys)
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            

            train_dataframe = DataValidation.read_data(file_path=train_file_path)
            test_dataframe = DataValidation.read_data(file_path=test_file_path)
            

            #validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"Train files has different number of columns"
                raise Exception(error_message)

            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"Test files has different number of columns"
                raise Exception(error_message)
            logging.info("validated number of columns")
            
            
            #validate numerical columns
            status = self.numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message = f"Train files has different number of numerical columns"
                raise Exception(error_message)

            status = self.numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message = f"Test files has different number of numerical columns"
                raise Exception(error_message)
            logging.info("validated number of numerical columns")
            
            
            #validate dataset drift
            status = self.detect_dataset_drift(base=train_dataframe,current=test_dataframe)

            if status:
                error_message = f"Data Drift detected between train and test dataset"
                raise Exception(error_message)
            logging.info("validated dataset drift")
            
            datavalidationartifact = DataValidationArtifact(
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                is_validated=True,
                message="Data validation completed successfully",
                error_message=None,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            
            logging.info(f"Data validation artifact: {datavalidationartifact}")
            return datavalidationartifact
        
        except Exception as e:
            raise SensorException(e,sys)
                
            