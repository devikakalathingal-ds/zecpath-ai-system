from sklearn.metrics.pairwise import cosine_similarity

def get_similarity(emb1, emb2):
    """
    Calculate cosine similarity between two embeddings
    """
    score = cosine_similarity([emb1], [emb2])[0][0]
    return score