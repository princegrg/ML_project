#feature engineering and data cleaning
import sys, os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformConfig: #this will give defualt path ways needed
    preprocess_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transform_config = DataTransformConfig()
    
    def get_transformer(self):
        try:
            num_feat = ['math score', 'reading score']
            cat_feat = [
                'gender',
                'race',
                'parental level of education',
                'lunch',
                'test preparation course',
            ]

            num_pipeline = Pipeline(
                steps = [
                    ('imputer', SimpleImputer(strategy = 'median')), #this handles the missing values by replacing the missing values with the median value
                    ('scaler', StandardScaler(with_mean = False)), #this peforms the standard scalingfor numerical values
                ]
            )

            cat_pipeline = Pipeline(
                steps = [
                    ('imputer', SimpleImputer(strategy = 'most_frequent')), #this handles the missing values
                    ('one_hot_encoder', OneHotEncoder()), #this peforms the OH encoding for categorical values
                    ('scaler', StandardScaler(with_mean = False)), #this peforms the standard scaling for numerical values
                ]
            )
            logging.info('numerical columns standard scaling completed')
            logging.info('categorical columns encoding completed')

            preprocessor = ColumnTransformer(
                [
                ("num_pipeline", num_pipeline, num_feat),
                ('cat_pipeline', cat_pipeline, cat_feat)
                ]
            )

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transform(self, training_path, testing_path):
        try:
            training_set = pd.read_csv(training_path)
            testing_set = pd.read_csv(testing_path)

            logging.info('read datasets completed')

            preprocessors = self.get_transformer()
            logging.info('preprocessort gotten')

            target_feat = 'average score'
            num_feat = ['math score', 'reading score']
            cat_feat = [
                'gender',
                'race',
                'parental level of education',
                'lunch',
                'test preparation course',
            ]

            input_train_df = training_set.drop(columns = [target_feat], axis = 1)
            target_train_df = training_set[target_feat]

            input_test_df = testing_set.drop(columns = [target_feat], axis = 1)
            target_test_df = testing_set[target_feat]

            input_train_after = preprocessors.fit_transform(input_train_df)
            input_test_after = preprocessors.transform(input_test_df)
            
            train_array = np.c_[
                input_train_after, np.array(target_train_df)
            ] #this combines the preprocesse inpuot data and the target data
            test_array = np.c_[
                input_test_after, np.array(target_test_df)
            ]

            logging.info('applied preprocessing')

            save_object(
                file_path = self.data_transform_config.preprocess_path,
                obj_to_save = preprocessors
            )

            return (
                train_array,
                test_array, 
                self.data_transform_config.preprocess_path
            )
        except Exception as e:
            raise CustomException(e, sys)