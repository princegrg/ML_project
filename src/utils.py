import os, sys
import numpy as np
import pandas as pd
import dill
from src.exception import CustomException

def save_object(file_path, obj_to_save): #this saves the object in the specified path 
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok = True)
        with open(file_path, 'wb') as file_object:
            dill.dump(obj_to_save, file_object)
    except Exception as e:
        raise CustomException(e, sys)
