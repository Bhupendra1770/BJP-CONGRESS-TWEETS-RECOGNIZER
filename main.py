from Tweets_classifier.pipeline import prediction

if __name__=="__main__":
     try:
          prediction.start_prediction()
     except Exception as e:
          print(e)