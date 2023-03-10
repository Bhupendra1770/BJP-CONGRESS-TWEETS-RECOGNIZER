import sys,os
from Tweets_classifier.logger import logging
from Tweets_classifier.exception import SensorException
from Tweets_classifier.entity import config_entity
from Tweets_classifier.components.data_ingestion import DataIngestion
from Tweets_classifier.components.data_transformation import DataTransformation

def start_training_pipeline():
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()


        #data transformation
        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
        data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
    except Exception as e:
        raise SensorException(e, sys)
    


    


