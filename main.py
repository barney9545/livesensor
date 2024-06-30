from sensor.exception import SensorException
import sys
import os
from sensor.components.data_ingestion import DataIngestion
from sensor.entity.config_entity import DataingestionConfig, TrainingPipelineConfig
from sensor.data_access.sensor_data import SensorData
from sensor.pipeline.training_pipeline import TrainingPipeline
if __name__ == "__main__":

    try:
        pp1 = TrainingPipeline()
        pp1.run_pipeline()
        
    except Exception as e:
        raise SensorException(e,sys)

            

    # try:
    #     try:
    #         1/0
    #     except Exception as e:
    #         #print(e)
    #         raise SensorException(e,sys)
    # #this raises an exception and call the sensorException
    # #which again raises an exception
    # #to print just the custom error
    # except SensorException as e:
    #     print (e)