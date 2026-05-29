import faiss
import numpy as np

def build_index(embeddings):


    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        np.array(embeddings)
    )

    return index


def retrieve(
query_embedding,
index,
chunks,
k=3
):


    distances, indices = index.search(
        np.array([query_embedding]),
        k
    )

    return [
        chunks[i]
        for i in indices[0]
    ]

