from typing import Tuple
import numpy as np
from yt_gif_maker.embed import embed_query, embed_chunks
from yt_gif_maker.chunk import create_all


def find_closest(query: str, normalized_embeddings: np.array, chunks: list, pointers: list) -> Tuple[list, list]:
    query_embedding = embed_query(query)
    query_normalized_embedding = query_embedding / np.dot(query_embedding, query_embedding.T)
    consts = np.dot(normalized_embeddings, query_normalized_embedding.T)
    consts_sorted_indices = list(np.argsort(consts, axis=0)[::-1])
    consts_sorted_indices = [v[0] for v in consts_sorted_indices][:5]
    closest_chunks = [chunks[v] for v in consts_sorted_indices]
    closest_pointers = [pointers[v] for v in consts_sorted_indices]
    return closest_chunks, closest_pointers


def create_result_time_range(timestamped_words: list, closest_pointers: list):
    time_ranges = []
    for ind, pointer_set in enumerate(closest_pointers):
        start_word = timestamped_words[closest_pointers[ind][0]]
        end_word = timestamped_words[closest_pointers[ind][1]]

        start_time = int(start_word["start"] * 1000) - 50
        end_time = int(end_word["end"] * 1000) + 50
        
        time_range = [start_time, end_time]
        time_ranges.append(time_range)
    return time_ranges


def get_nearest_snippets(query: str, transcript: str, timestamped_words: list) -> list:
    chunks, pointers = create_all(query, transcript)
    normalized_chunk_embeddings = embed_chunks(chunks)
    closest_chunks, closest_pointers = find_closest(query, normalized_chunk_embeddings, chunks, pointers)
    closest_time_ranges = create_result_time_range(timestamped_words, closest_pointers)
    return closest_time_ranges