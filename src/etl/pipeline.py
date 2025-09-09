from src.etl.abstractions import Extractor, Transformer, Loader

class Pipeline:
    def __init__(self, extractor: Extractor, transformer: Transformer, loader: Loader):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self):
        extracted_data = self.extractor.extract()
        transformed_data = self.transformer.transform(extracted_data)
        self.loader.load(transformed_data)
