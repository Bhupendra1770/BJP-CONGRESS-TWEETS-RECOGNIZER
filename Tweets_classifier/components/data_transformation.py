import os,sys 
import pandas as pd
import numpy as np
import nltk
import string
from Tweets_classifier import utils
from Tweets_classifier.entity import artifact_entity,config_entity
from Tweets_classifier.exception import SensorException
from Tweets_classifier.logger import logging
from typing import Optional
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from Tweets_classifier.connection import TARGET_COLUMN



class DataTransformation:


    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)



    def initiate_data_transformation(self,) -> artifact_entity.DataTransformationArtifact:
        try:
            #reading training and testing file
            df = pd.read_csv(self.data_ingestion_artifact.feature_store_file_path)
            logging.info("dropping some unwanted columns")

            if 'Unnamed: 0.1' in df.columns:
                df.drop('Unnamed: 0.1',axis=1,inplace=True)
            elif 'Unnamed: 0' in df.columns:
                df.drop('Unnamed: 0',axis=1,inplace=True)
            else:
                pass
            
            logging.info("droping duplicate values if exist")
            df.drop_duplicates(inplace=True)

            logging.info("adding one column as clean_tweets")
            df['clean_tweets'] = df['tweet'].str.replace("[^a-zA-Z#]", " ")

            logging.info("dropping old tweet column")
            df = df.drop(columns=['tweet'])

            nltk.download('punkt')

            ps = PorterStemmer()

            logging.info(df.head())
            logging.info("transforming tweet and create a new column known as transformed_tweets")

            l = []
            for i in (list(df['clean_tweets'])):

                clean_tweet = i.lower()
                clean_tweet = nltk.word_tokenize(clean_tweet)
                
                y = []
                for i in clean_tweet:
                    if i.isalnum():
                        y.append(i)
                
                clean_tweet = y[:]
                y.clear()
                
                for i in clean_tweet:
                    if i not in stopwords.words('english') and i not in string.punctuation:
                        y.append(i)
                        
                clean_tweet = y[:]
                y.clear()
                
                ps = PorterStemmer()

                for i in clean_tweet:
                    y.append(ps.stem(i))
                
                        
                l.append(" ".join(y))


            df["transformed_tweets"] = l
            logging.info("transformed succefully")
            logging.info(df.head())


            logging.info("dropping clean_tweets column")
            df.drop('clean_tweets',axis=1,inplace=True)
            logging.info(df.columns)



            logging.info("converting transformed tweets to vector with the help of countvectorizer")
            cv = CountVectorizer(max_features=14070)
            feature = cv.fit_transform(df['transformed_tweets']).toarray()

            logging.info("extracting our both target columns")
            target = df['target'].values


            logging.info("saving all numpy array and object")
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_feature_path,
                                        array=feature)

            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_target_path,
                                        array=target)


            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
             obj=cv)



            logging.info("generating artifact")
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_feature_path = self.data_transformation_config.transformed_feature_path,
                transformed_target_path = self.data_transformation_config.transformed_target_path,

            )

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)