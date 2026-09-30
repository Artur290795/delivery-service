from sentence_transformers import SentenceTransformer



class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(model_name_or_path="paraphrase-multilingual-MiniLM-L12-v2")

    def convert_text_to_vector(self, text: str) -> list[float]:
        vector = self.model.encode(text)
        return list(vector)
