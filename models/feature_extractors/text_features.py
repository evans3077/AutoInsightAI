from transformers import pipeline as hf_pipeline

class TextFeatureExtractor:
    def __init__(self):
        self.nlp = hf_pipeline("feature-extraction", model="distilbert-base-uncased")

    def extract(self, text: str):
        features = self.nlp(text)
        return features
