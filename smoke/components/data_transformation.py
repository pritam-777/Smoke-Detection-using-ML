import numpy as np
import pandas as pd
import os
import sys
from smoke.logger import logging
from smoke.exception import SmokeException
from smoke.entity import artifact_entity,config_entity
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from smoke.config import TARGET_COLUMN
from smoke.config import UNWANTED_COLUMNS
from smoke import utils

class DataTransformation:


    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise SmokeException(e, sys)


    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy='constant', fill_value=0)
            robust_scaler =  RobustScaler()
            pipeline = Pipeline(steps=[
                    ('Imputer',simple_imputer),
                    ('RobustScaler',robust_scaler)
                ])
            return pipeline
        except Exception as e:
            raise SmokeException(e, sys)


    def initiate_data_transformation(self,) -> artifact_entity.DataTransformationArtifact:
        try:
            #reading training and testing file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            #selecting input feature for train and test dataframe
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)


            input_feature_train_df=train_df.drop(UNWANTED_COLUMNS,axis=1)
            input_feature_test_df=test_df.drop(UNWANTED_COLUMNS,axis=1)

            #selecting target feature for train and test dataframe
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]





            transformation_pipleine = DataTransformation.get_data_transformer_object()
            transformation_pipleine.fit(input_feature_train_df)

            #transforming input features
            input_feature_train_arr = transformation_pipleine.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipleine.transform(input_feature_test_df)
            

            smt = SMOTETomek(sampling_strategy='auto',random_state=1)
            logging.info(f"Before resampling in training set Input: {input_feature_train_arr.shape} Target:{target_feature_train_df.shape}")
            input_feature_train_arr, target_feature_train_arr = smt.fit_resample(input_feature_train_arr, target_feature_train_df)
            logging.info(f"After resampling in training set Input: {input_feature_train_arr.shape} Target:{target_feature_train_df.shape}")
            
            logging.info(f"Before resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_df.shape}")
            input_feature_test_arr, target_feature_test_arr = smt.fit_resample(input_feature_test_arr, target_feature_test_df)
            logging.info(f"After resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_df.shape}")

            #target encoder
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr ]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]


            #save numpy array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,
                                        array=train_arr)

            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,
                                        array=test_arr)


            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
             obj=transformation_pipleine)



            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,

            )

            logging.info(f"Data transformation object {data_transformation_artifact}")
            logging.info(f"{'>>'*20} Data Transformation Artifact{'<<'*20}")
            return data_transformation_artifact
        except Exception as e:
            raise SmokeException(e, sys)


