import os,sys
from Tweets_classifier.exception import SensorException
from Tweets_classifier.logger import logging
from datetime import datetime

FILE_NAME = "Tweets.csv"
INPUT_FEATURE_FILE_NAME = "feature.npz"
TARGET_FILE_NAME = "target.npz"
PARTY_FILE_NAME = "party.npz"
TRANSFORMER_OBJECT_FILE_NAME = "cv_transformer.pkl"
MODEL_FILE_NAME = "model.pkl"


class TrainingPipelineConfig:

    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception  as e:
            raise SensorException(e,sys)     
        

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.DATA_FILE_PATH="https://raw.githubusercontent.com/Bhupendra1770/BJP-CONGRESS-TWEETS-RECOGNIZER/main/Tweets.csv"
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir , "data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)

        except Exception as e:
            return SensorException(e,sys)
        



class DataValidationConfig:
    pass


        

class DataTransformationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir , "data_transformation")
            self.transform_object_path = os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_FILE_NAME)
            self.transformed_feature_path =  os.path.join(self.data_transformation_dir,"transformed",INPUT_FEATURE_FILE_NAME)
            self.transformed_target_path =os.path.join(self.data_transformation_dir,"transformed",TARGET_FILE_NAME)


        except Exception as e:
            return SensorException(e,sys)


class ModelTrainerConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir , "model_trainer")
        self.model_path = os.path.join(self.model_trainer_dir,"model",MODEL_FILE_NAME)
        self.expected_score = 0.8


class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.change_threshold = 0.01

class ModelPusherConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_pusher_dir = os.path.join(training_pipeline_config.artifact_dir , "model_pusher")
        self.saved_model_dir = os.path.join("saved_models")
        self.pusher_model_dir = os.path.join(self.model_pusher_dir,"saved_models")
        self.pusher_model_path = os.path.join(self.pusher_model_dir,MODEL_FILE_NAME)
        self.pusher_transformer_path = os.path.join(self.pusher_model_dir,TRANSFORMER_OBJECT_FILE_NAME)
