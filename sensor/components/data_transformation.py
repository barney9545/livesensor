import os,sys
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import save_numpy_array_data, load_numpy_array_data, save_object
from sensor.entity.config_entity import DataTransformationConfig,TrainingPipelineConfig
from sensor.entity.artifacts_entity import DataTransformationArtifact,DataIngestionArtifact,DataValidationArtifact
from sensor.ml.model.estimator import TargetValueMapping
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.components.data_validation import DataValidation

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.preprocessing import RobustScaler
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline


class DataTransformation:
    
    def __init__(self,data_transformation_config:DataTransformationConfig,
                 data_validation_artifact:DataValidationArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation Initiated. {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        
        except Exception as e:
            raise SensorException(e,sys)
    
    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            robust_scaler = RobustScaler()
            #knn_imputer = KNNImputer(n_neighbors=5, weights='distance')
            #pre_processor = Pipeline(steps=[("scaler",robust_scaler),("imputer",knn_imputer)])
            simple_imputer = SimpleImputer(strategy='constant', fill_value=0)
            pre_processor = Pipeline(steps=[("imputer",simple_imputer),("scaler",robust_scaler)])
            
            logging.info("Pre Processing Pipeline created successfully")
            return pre_processor
        except Exception as e:
            raise SensorException(e,sys)
    
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Initiating data transformation")
            train_file_path = self.data_validation_artifact.valid_train_file_path
            test_file_path = self.data_validation_artifact.valid_test_file_path
            
            train_df = DataValidation.read_data(file_path=train_file_path)
            test_df = DataValidation.read_data(file_path=test_file_path)
            logging.info("Read train and test data successfully")
            pipeline = self.get_data_transformer_object()
            
            input_train_feature = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_train_feature = train_df[TARGET_COLUMN].replace(TargetValueMapping().to_dict())
            
            logging.info("Train set created successfully")
            
            input_test_feature = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_test_feature = test_df[TARGET_COLUMN].replace(TargetValueMapping().to_dict())
            
            logging.info("Test set created successfully")
            
            pipeline.fit(input_train_feature)
            logging.info("Pipeline fitted successfully")
            input_train_feature = pipeline.transform(input_train_feature)
            input_test_feature = pipeline.transform(input_test_feature)
            logging.info("Data transformed successfully")
            
            logging.info("smote started")
            smt = SMOTE(sampling_strategy='minority',random_state=32)
            
            input_train_feature, target_train_feature = smt.fit_resample(input_train_feature, target_train_feature)
            input_test_feature, target_test_feature = smt.fit_resample(input_test_feature, target_test_feature)
            logging.info("Resampling completed")
            
            train_arr = np.c_[input_train_feature, np.array(target_train_feature)]
            logging.info(f"train array created successfully: {train_arr.shape}")
            test_arr = np.c_[input_test_feature, np.array(target_test_feature)]
            logging.info("data converted to arrays")
            
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path, array= test_arr)
            
            save_object(file_path=self.data_transformation_config.transformed_object_file_path, obj=pipeline)
            
            #preparing artifact
            
            data_transformation_artifact = DataTransformationArtifact(
                
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path= self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
                is_transformed= True,
                message="Data transformation successfull",
                error_message=None
            )           
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        
        except Exception as e:
            raise SensorException(e,sys)