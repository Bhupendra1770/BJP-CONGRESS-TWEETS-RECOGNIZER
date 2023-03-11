from Tweets_classifier.entity import artifact_entity,config_entity
from Tweets_classifier.exception import SensorException
from Tweets_classifier.logger import logging
from typing import Optional
import os,sys 
from sklearn.ensemble import ExtraTreesClassifier
from Tweets_classifier import utils
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split


class ModelTrainer:


    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact
                ):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)


    def train_model(self,x,y):
        try:
            xtr_clf =  ExtraTreesClassifier(n_jobs=-1)
            xtr_clf.fit(x,y)
            return xtr_clf
        except Exception as e:
            raise SensorException(e, sys)


    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Loading input feature and target feature.")
            feature_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_feature_path)
            target_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_target_path)

            logging.info(f"Splitting into train and test.")
            x_train,x_test,y_train,y_test = train_test_split(feature_arr,target_arr,test_size=0.2,random_state=7)

            logging.info(f"Train the model")
            model = self.train_model(x=x_train,y=y_train)

            logging.info(f"Calculating f1 train score")
            yhat_train = model.predict(x_train)
            f1_train_score  =f1_score(y_true=y_train, y_pred=yhat_train)

            logging.info(f"Calculating f1 test score")
            yhat_test = model.predict(x_test)
            f1_test_score  =f1_score(y_true=y_test, y_pred=yhat_test)
            
            logging.info(f"train score:{f1_train_score} and tests score {f1_test_score}")

            #save the trained model
            logging.info(f"Saving mode object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            #prepare artifact
            logging.info(f"Prepare the artifact")
            model_trainer_artifact  = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path,)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)



