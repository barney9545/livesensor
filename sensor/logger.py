import sys
import os
import logging
from datetime import datetime as dt

log_file = f"{dt.now().strftime(format= '%d_%m_%Y_%H_%M_%S')}.log"

log_path = os.path.join(os.getcwd(),"logs",log_file)

os.makedirs(log_path,exist_ok=True)

log_file_path = os.path.join(log_path,log_file)


logging.basicConfig(
    filename= log_file_path,
    format="[%(asctime)s]- %(lineno)d-%(name)s-%(levelname)s -- %(message)s" ,
    level=logging.INFO

)

if __name__ == "__main__":
    logging.info("logging has started")
