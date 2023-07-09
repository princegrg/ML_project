import logging #module in Python is a built-in module that provides a flexible framework for recording log messages from your application.
import os
from datetime import datetime

#the purpose of this file is to log all the executions, or exception into this file so that we can backtrack if needed

log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" #this returns a datetime object into a string representation in the specified format
log_path = os.path.join(os.getcwd(), "logs", log_file)
os.makedirs(log_path, exist_ok = True)

log_file_path = os.path.join(log_path, log_file)

logging.basicConfig(
    filename = log_file_path, #specfies the path to the file where the log records will be written, expected to be a string
    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s", #this specifies the format of each log record based on when and where the logging call was made and who made the call, as well as the actual message 
    level = logging.INFO, #this specifies the threshold level for the logs to be written in this case, the level is INFO, so INFO, WARNING, ERROR, CRITICAL will be written to the log file

) #this sets up the basic configuration for the loggin module
