import numpy as np
import json
from sentence_transformers import SentenceTransformer
from typing import List, Dict

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text: str) -> np.ndarray:
    """Convert text into a vector embedding."""
    return np.array(model.encode(text, convert_to_numpy=True))


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def compute_relevance(current_situation: str, memory_text: str) -> float:
    """Compute semantic similarity between the current situation and a memory."""
    situation_embedding = embed_text(current_situation)
    memory_embedding = embed_text(memory_text)
    return cosine_similarity(situation_embedding, memory_embedding)

def retrieve_top_memories(json_path, current_situation, current_step, top_n=5,
                          w_importance=0.4, w_relevance=0.4, w_recency=0.2):
    # Load memories from JSON
    with open(json_path, "r") as f:
        memories = json.load(f)

    # Embed current situation once
    situation_vec = embed_text(current_situation)

    scored_memories = []
    for memory in memories:
        # Compute relevance
        memory_vec = embed_text(memory["text"])
        relevance = cosine_similarity(situation_vec, memory_vec)

        # Compute recency (normalized)
        recency = 1 / (1 + max(0, current_step - memory.get("simulationstep", 0)))

        # Importance (already in memory)
        importance = memory.get("importance", 0)

        # Weighted score
        retrieval_score = (
            w_importance * importance +
            w_relevance  * relevance +
            w_recency    * recency
        )

        memory["relevance"] = relevance
        memory["recency"] = recency
        memory["retrieval_score"] = retrieval_score
        scored_memories.append(memory)

    # Sort by retrieval score
    scored_memories.sort(key=lambda m: m["retrieval_score"], reverse=True)

    # Return the top N
    return scored_memories[:top_n]