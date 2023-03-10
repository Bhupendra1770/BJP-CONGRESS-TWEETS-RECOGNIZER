import sys,os
from Tweets_classifier.logger import logging
from Tweets_classifier.exception import SensorException
from Tweets_classifier.entity import config_entity
from Tweets_classifier.components.data_ingestion import DataIngestion

def start_training_pipeline():
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    except Exception as e:
        raise SensorException(e, sys)
    
