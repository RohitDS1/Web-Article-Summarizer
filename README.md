# Web Article Summarizer
The Web Article Summarizer is a tool designed to summarize and analyze articles or news content from a provided URL. The application is created based on several significant steps including preprocessing of the data, modeling, and prediction using multiple NLP technology.

## Content Table
1. [Overview](#implementation-overview)
2. [Data](#data-for-training)
3. [Models & Techniques](#models-and-techniques)
4. [Input Processing](#input-processing)
5. [Interface](#front-end-gui)
6. [Future Development](#future-development)
7. [License](#license)

## Implementation Overview
Our application's models are trained on a dataset provided by Benzinga News, and optimized using the SimHash methodology for deduplication. The refined data deduplicated with Simhash powers the training of two models: Named Entity Recognition (NER) via Spacy and Latent Dirichlet Allocation (LDA) using Scikit-Learn. These models parse and analyze a user-inputted URL, identifying key entities and topics. In addition, a pre-trained T5 transformer model is also used to perform summarization tasks on the article title and body. This ensures that the user receives a concise and contextually accurate synopsis of the content. The summarized and analyzed output is then presented through an intuitive GUI, offering the user a concise and comprehensive understanding of any given web article.

## Data for training
The initial stage of the Web_Article_Summarizer is data collection. It utilizes the data from Benzinga News, which serves as the primary source of information to train our models. We used Benzinga's API and extracted the date, title, and body fields for training purposes. This raw data is then preprocessed using the SimHash methodology, which aids in the removal of duplicate news articles. 
<br/><br/> The data initially has 14072 rows. After deduplication, 1130 rows are marked duplicated and there are 12942 rows left in the train set data. This deduplication is a crucial step as it ensures that our model is trained on unique and diverse data, thus avoiding bias in predictions. 

## Models and Techniques
The training phase begins once the data has been cleaned and prepared. By far, four primary techniques are applied in this phase: 
<br/><br/> 1. Deduplication by Simhash algorithm. 
<br/><br/> 2. Named Entity Recognition (NER) using the Spacy library. 
<br/><br/> 3. Latent Dirichlet Allocation (LDA) for topic modeling via Scikit-Learn. 
<br/><br/> 4. Pre-trained T5 transformers for summarization.
<br/><br/> Firstly, the SimHash methodology is employed for data deduplication, ensuring our models are trained on unique and diverse news data. This is a crucial step in refining the quality of the dataset.NER is then employed to identify and classify named entities in the text, such as people, organizations, locations, etc. Concurrently, the LDA method helps in discerning the main topics present in the text data. Lastly, T5, a transformer pre-trained model, is used to provide succinct summaries of the articles' titles and bodies. This allows for a more granular and effective summarization, which contributes significantly to the final analysis.
<br/><br/> All these models and techniques are trained on the preprocessed news data, thereby ensuring highly accurate and insightful text summarization and analysis.

## Input Processing
In the operational phase, when a user inputs a URL, the system built with Pypputeer parses the content from the URL and processes it using the trained models. The NER model identifies the named entities in the article, while the LDA model determines the topics discussed in the article.

## Front-end GUI
The results obtained from the models are then computed to form the final summary and analysis of the article. The summary, including identified entities and topics, is presented to the user through an interactive GUI.

## Future Development
We are prepared for any future changes including adding new features and model optimization.

## License
MIT education license
