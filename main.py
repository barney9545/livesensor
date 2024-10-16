from sensor.exception import SensorException
from sensor.logger import logging
import sys
import os
from sensor.components.data_ingestion import DataIngestion
from sensor.entity.config_entity import DataingestionConfig, TrainingPipelineConfig
from sensor.data_access.sensor_data import SensorData
from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.constant.application import APP_HOST,APP_PORT
from sensor.utils.main_utils import load_object
from sensor.ml.model.estimator import TargetValueMapping, SensorModel, ModelResolver
from fastapi import FastAPI,File,UploadFile,Response
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run
import pandas as pd
from starlette.responses import RedirectResponse #to redirect to /docs page


try:
    app = FastAPI()
    
    origins =["*"]
    #cross-origin resource sharing
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/",tags=["authentication"])
    async def index():
        return RedirectResponse(url="/docs")
    
    @app.get("/train")
    async def main():
        try:
            pp1 = TrainingPipeline()
            if pp1.is_pipeline_running():
                return Response("Training is in progress, please wait until it ends")
            pp1.run_pipeline()
            return Response("Training successful!")
        
        except Exception as e:
            logging.info(e)
            return Response(f"Error Occurred! {e}")
    
    #@app.get("/predict")
    
        
except Exception as e:
    raise SensorException(e,sys)

if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)
    

            

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