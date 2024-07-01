from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str
    is_ingested:bool
    message:str
    error_message:str
    
@dataclass
class DataValidationArtifact:
    valid_train_file_path:str
    valid_test_file_path:str
    drift_report_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    is_validated:bool
    message:str
    error_message:str
    
@dataclass
class DataTransformationArtifact:
    transformed_train_file_path:str
    transformed_test_file_path:str
    transformed_object_file_path:str
    is_transformed:bool
    message:str
    error_message:str

@dataclass
class ClassificationMetricArtifact:
    f1_score:float
    precision_score:float
    recall_score:float
    accuracy_score:float
    roc_auc_score:float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str
    train_metric_artifact:ClassificationMetricArtifact
    test_metric_artifact:ClassificationMetricArtifact
    is_trained:bool
    message:str
    error_message:str

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    improved_accuracy:float
    best_model_path:str
    trained_model_path:str
    train_model_metric_artifact:ClassificationMetricArtifact
    best_model_metric_artifact:ClassificationMetricArtifact
    message:str
    error_message:str

@dataclass
class ModelPusherArtifact:
    saved_model_path:str
    model_file_path:str
    message:str
    error_message:str