from models.feature_extractors.image_features import ImageFeatureExtractor
from models.feature_extractors.text_features import TextFeatureExtractor

class MLPipeline:
    def __init__(self):
        self.image_extractor = ImageFeatureExtractor()
        self.text_extractor = TextFeatureExtractor()

    def process_image(self, image_path):
        return self.image_extractor.extract(image_path)

    def process_text(self, text):
        return self.text_extractor.extract(text)

pipeline = MLPipeline()
