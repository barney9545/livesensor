import os,sys
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity.artifacts_entity import ClassificationMetricArtifact

from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score



def get_classification_metric(actual,predicted)->ClassificationMetricArtifact:
    try:
        model_accuracy = accuracy_score(actual,predicted)
        model_precision = precision_score(actual,predicted)
        model_recall = recall_score(actual,predicted)
        model_f1 = f1_score(actual,predicted)
        model_roc_auc = roc_auc_score(actual,predicted)
        
        classification_artifact = ClassificationMetricArtifact(
            f1_score=model_f1,
            precision_score=model_precision,
            recall_score=model_recall,
            accuracy_score=model_accuracy,
            roc_auc_score=model_roc_auc
        )

        logging.info(f"Classification metric artifact: {classification_artifact}")
        return classification_artifact

    except Exception as e:
        raise SensorException(e,sys) from e