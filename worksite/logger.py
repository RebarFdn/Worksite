
import logging
from pathlib import Path
from loguru import logger as log
from config import LOG_PATH


gurulog_file_path:Path = LOG_PATH / 'guru.log' 
log.add(gurulog_file_path, rotation="10 MB", retention="100 days", level="INFO", compression="zip")

# Python standard logger
def logger():
    # Create and configure logger
    logging.basicConfig(filename=LOG_PATH /'program_log.log',
                    format='%(asctime)s %(message)s',
                    filemode='w') 
    # Creating an object
    logger = logging.getLogger() 
    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.INFO)
    return logger
 

# logguru logger
def guru_logger(message:str=""):
    if message:
        log.info(message)   
    return log

g_log = guru_logger()