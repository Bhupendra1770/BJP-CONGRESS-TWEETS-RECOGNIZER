import os,sys
from Tweets_classifier.exception import SensorException
from Tweets_classifier.logger import logging
from datetime import datetime

FILE_NAME = "Tweets.csv"


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