from Tweets_classifier.pipeline.training_pipeline import start_training_pipeline

print(__name__)
if __name__=="__main__":
     try:
          start_training_pipeline()
     except Exception as e:
          print(e)