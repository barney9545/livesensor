import os,sys
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import save_numpy_array_data, load_numpy_array_data, save_object, load_object
from sensor.entity.config_entity import ModelEvaluationConfig
from sensor.entity.artifacts_entity import DataValidationArtifact,DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact, ModelEvaluationArtifact
from sensor.ml.metric.classification_metric import get_classification_metric
from sensor.ml.model.estimator import SensorModel, TargetValueMapping , ModelResolver
import pandas as pd
from sensor.constant.training_pipeline import TARGET_COLUMN

class ModelEvaluation:

    def __init__(self, model_evaluation_config:ModelEvaluationConfig, 
                 data_validation_artifact:DataValidationArtifact,
                 model_trainer_artifact:ModelTrainerArtifact):
        try:
            logging.info(f"{'>>'*20}Model Evaluation log started.{'<<'*20}")
            self.model_evaluation_config = model_evaluation_config
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys) from e
    
    def intiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path
            valid_test_file_path = self.data_validation_artifact.valid_test_file_path
            
            train_df = pd.read_csv(valid_train_file_path)
            test_df = pd.read_csv(valid_test_file_path)
            
            x_train = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            y_train = train_df[TARGET_COLUMN].replace(TargetValueMapping().to_dict())
            
            x_test = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            y_test = test_df[TARGET_COLUMN].replace(TargetValueMapping().to_dict())
            
            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            
            modelresolver = ModelResolver()
            is_model_accepted = True
            if not modelresolver.check_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=True,
                                                                    improved_accuracy=None,
                                                                    best_model_path=None,
                                                                    trained_model_path=trained_model_file_path,
                                                                    train_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact,
                                                                    best_model_metric_artifact=None,
                                                                    message="Model evaluation completed successfully. Model not found. Hence accepting trained model",
                                                                    error_message=None)
                                            
                logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact
            
            latest_model_path = modelresolver.get_latest_model_path()
            latest_model = load_object(file_path=latest_model_path)
            trained_model = load_object(file_path=trained_model_file_path)
            
            y_trained_pred = trained_model.predict(x_test)
            y_latest_pred = latest_model.predict(x_test)
            
            trained_metric = get_classification_metric(actual=y_test,predicted=y_trained_pred)
            latest_metric = get_classification_metric(actual=y_test,predicted=y_latest_pred)
            
            logging.info(f"trained metric: {trained_metric} latest metric: {latest_metric}")
            
            delta_accuracy = latest_metric.f1_score - trained_metric.f1_score
            
            if delta_accuracy > self.model_evaluation_config.model_evaluation_threshold:
                is_model_accepted= True
            else:
                is_model_accepted= False
            
            model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=is_model_accepted,
                                            improved_accuracy=delta_accuracy,
                                            best_model_path=latest_model_path,
                                            trained_model_path=trained_model_file_path,
                                            train_model_metric_artifact=trained_metric,
                                            best_model_metric_artifact=latest_metric,
                                            message="Model evaluation completed successfully. Model accepted",
                                            error_message=None)
            
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            
            return model_evaluation_artifact
            
        except Exception as e:
            raise SensorException(e,sys) from e