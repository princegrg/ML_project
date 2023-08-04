import os, sys
import numpy as np
import pandas as pd
import dill
from src.exception import CustomException
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

def save_object(file_path, obj_to_save): #this saves the object in the specified path 
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok = True)
        with open(file_path, 'wb') as file_object:
            dill.dump(obj_to_save, file_object)
    except Exception as e:
        raise CustomException(e, sys)

def model_evaluate(x_train, y_train, x_test, y_test, models):
    try:
        list_of_metrics = {}

        for a in range(len(list(models))):
            model_name = list(models.keys())[a] #this gets the name of the individual model
            model_instance = list(models.values())[a] #this gets the individual model, and the value which is the actual instance of the model
            model_instance.fit(x_train, y_train) #this trains the model
            test_pred = model_instance.predict(x_test)#this is the prediction with the testing inputs

            testing_score = r2_score(y_test, test_pred)#this gets the r2 score by comparing the prediction with the actual labels for the testing dataset

            list_of_metrics[model_name] = testing_score#this will match the key value pair for each model and the respective r2 score
        
        return list_of_metrics
    except Exception as e:
        raise CustomException(e, sys)
