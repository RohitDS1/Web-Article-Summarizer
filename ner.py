import spacy

class NER():
    """
    Named Entity Recognition (NER) Class:

    This class provides functionality for detecting and classifying named entities in a given text based on a pre-trained
    model using the spaCy library.

    Key Features:
    1. The underlying NER model was trained using spaCy's neural network capabilities on custom training data.
    2. The trained model is loaded from the "model_train\model" directory.
    3. The class provides a method to extract named entities from a text and label them into predefined categories such 
       as "PERSON", "GPE" (Geopolitical Entity), "ORG" (Organization), "PERCENT", and "EVENT".

    How To Use:
    - Create an instance of the NER class.
    - Use the "ner" method on a text input to get a list of named entities along with their corresponding labels.

    Note:
    The training code prior to this class leveraged spaCy's capabilities to train the NER model on custom news data.
    The model was trained to recognize five entity labels: "PERSON", "GPE", "ORG", "PERCENT", and "EVENT".
    """
    def __init__(self) -> None:
        self.nlp = spacy.load("model_train\model")

    def ner(self, text):
        doc = self.nlp(text)
        return [(ent.text, ent.label_)for ent in doc.ents]