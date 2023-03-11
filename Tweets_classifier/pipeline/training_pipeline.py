import sys,os
from Tweets_classifier.logger import logging
from Tweets_classifier.exception import SensorException
from Tweets_classifier.entity import config_entity
from Tweets_classifier.components.data_ingestion import DataIngestion
from Tweets_classifier.components.data_transformation import DataTransformation
from Tweets_classifier.components.model_trainer import ModelTrainer
from Tweets_classifier.components.model_evaluation import ModelEvaluation
from Tweets_classifier.components.model_pusher import ModelPusher

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

        #model trainer
        model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()

        #model evaluation
        model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_eval  = ModelEvaluation(model_eval_config=model_eval_config,
        data_ingestion_artifact=data_ingestion_artifact,
        data_transformation_artifact=data_transformation_artifact,
        model_trainer_artifact=model_trainer_artifact)
        model_eval_artifact = model_eval.initiate_model_evaluation()

        #model pusher
        model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config)
        
        model_pusher = ModelPusher(model_pusher_config=model_pusher_config, 
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_artifact=model_trainer_artifact)

        model_pusher_artifact = model_pusher.initiate_model_pusher()

    except Exception as e:
        raise SensorException(e, sys)
    


    


