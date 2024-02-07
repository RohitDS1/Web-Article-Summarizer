import pandas as pd
import pickle
import numpy as np
import nltk
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import dill

# To make this work, make sure lda_model.pkl and tf_vectorizer.pkl are in the model_train directory

def get_topic_keywords(lda_model, vectorizer, text, num_keywords):
    test_matrix = vectorizer.transform([text])
    test_lda_output = lda_model.transform(test_matrix)
    topic_names = ['Topic ' + str(i) for i in range(lda_model.n_components)]
    lda_output_df = pd.DataFrame(np.round(test_lda_output, 2), columns=topic_names)
    dominant_topic = np.argmax(lda_output_df.values, axis=1)[0]
    topics = lda_model.components_
    feature_names = vectorizer.get_feature_names_out()
    keywords = [feature_names[i].strip() for i in topics[dominant_topic].argsort()[:-num_keywords-1:-1]]
    keywords = list(dict.fromkeys(keywords))
    keywords_str = ", ".join(keywords)
    return dominant_topic, keywords_str


def tokenize_bodys(body):
    tokens = nltk.word_tokenize(body)
    lmtzr = WordNetLemmatizer()
    filtered_tokens = []
    
    for token in tokens:
        token = token.replace("'s", " ").replace("n’t", " not").replace("’ve", " have")
        token = re.sub(r'[^a-zA-Z0-9 ]', '', token)
        if token not in stopwords.words('english'):
            filtered_tokens.append(token.lower())
    
    lemmas = [lmtzr.lemmatize(t,'v') for t in filtered_tokens]
    return lemmas

def topic_model(text):
    with open('./model_train/lda_model.pkl', 'rb') as file:
        lda_model_loaded = dill.load(file)
    with open('./model_train/tf_vectorizer.pkl', 'rb') as file:
        tf_vectorizer_loaded = dill.load(file)
        
    dominant_topic, keywords = get_topic_keywords(lda_model_loaded, tf_vectorizer_loaded, text, 10)
    return f"Category: {dominant_topic}\nKeywords: {keywords}"