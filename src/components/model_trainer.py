import os
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
# Modelling
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from catboost import CatBoostRegressor
from src.utils import save_object, model_evaluate
from src.logger import logging
from src.exception import CustomException


@dataclass
class ModelTrainerConfig:
    model_path = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_training(self, train_after_array, test_after_array):
        try:
            logging.info('spliting training and testing data')
            x_train, y_train, x_test, y_test = (
                train_after_array[:,:-1],#this takes out everything except the last column, which would result in the input features
                train_after_array[:,-1],#this takes out the last column, which is the label columns
                test_after_array[:,:-1],#this takes out everything except the last column, which would result in the input features
                test_after_array[:,-1],#this takes out the last column, which is the label columns
            )
            models = {
                'random forest': RandomForestRegressor(),
                'linear regression': LinearRegression(),
                'decision tree': DecisionTreeRegressor(),
                'k-neighbors classifier': KNeighborsRegressor(),
                'catboosting classifier': CatBoostRegressor(verbose = False),
                'gradient boosting': GradientBoostingRegressor(),
            }
            model_metrics = model_evaluate(x_train, y_train, x_test, y_test, models)

            best_score = max(sorted(model_metrics.values())) #this gets the highest r2 score
            best_model_name = list(model_metrics.keys())[list(model_metrics.values()).index(best_score)] #this get the name of the model wiht the best score
            best_model_instance = models[best_model_name] #this  gets the instance of the best model

            logging.info('found the model')

            save_object(
                file_path = self.model_trainer_config.model_path,
                obj_to_save= best_model_instance
            ) #this save the instance of the model selected

            y_pred = best_model_instance.predict(x_test)
            r2_score_y = r2_score(y_test, y_pred)
            print(f'The best model is {best_model_name} with an r2 score of {r2_score_y}') #this will return the best model's r2 score after the prediction was made on the testing data
        except Exception as e:
            raise CustomException(e, sys)



