import pickle
import string
import streamlit as st
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
from Tweets_classifier import utils
from Tweets_classifier.predictor import ModelResolver


mr = ModelResolver()
def start_prediction():
    ps = PorterStemmer()
    cv_transformer = utils.load_object(file_path=mr.get_latest_transformer_path())
    model = utils.load_object(file_path=mr.get_latest_model_path())

    st.title("BJP-CONGRESS TWEET CLASSIFIER")

    input_sms = st.text_area("ENTER YOUR TWEET")

    if st.button('PREDICT'):
        # 1. preprocess
        transformed_tweet = utils.transform_text(input_sms)
        # 2. vectorize
        vector_input = cv_transformer.transform([transformed_tweet])
        # 3. predict
        result = model.predict(vector_input)[0]
        # 4. Display
        if result == 1:
            st.header("Its a Positive Comment")
        else:
            st.header("Its a Negative Comment")
