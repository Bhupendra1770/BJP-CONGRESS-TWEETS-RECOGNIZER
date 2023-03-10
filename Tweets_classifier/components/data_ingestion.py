from Tweets_classifier.entity import config_entity
from Tweets_classifier.entity import artifact_entity
from Tweets_classifier.exception import SensorException
from Tweets_classifier.logger import logging
import os,sys
import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split



class DataIngestion:
    
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig ):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)
        

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"Exporting collection data as pandas dataframe")
            df:pd.DataFrame  = pd.read_csv(self.data_ingestion_config.DATA_FILE_PATH)

            logging.info("Save data in feature store")


            logging.info("Create feature store folder if not available")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            logging.info("Save df to feature store folder")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)
            

            logging.info("Prepare artifact")
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(error_message=e, error_detail=sys)


