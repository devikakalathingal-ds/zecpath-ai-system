from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """
    Convert text into embedding vector
    """
    return model.encode(text)