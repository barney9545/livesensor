from sensor.exception import SensorException
import sys
import os

if __name__ == "__main__":
    try:
        try:
            1/0
        except Exception as e:
            #print(e)
            raise SensorException(e,sys)
    #this raises an exception and call the sensorException
    #which again raises an exception
    #to print just the custom error
    except SensorException as e:
        print (e)
    
   
        