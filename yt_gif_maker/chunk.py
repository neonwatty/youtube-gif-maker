import re
from typing import Tuple


def clean_word(text: str) -> str:
    # clean input text - keeping only lower case letters, numbers, punctuation, and single quote symbols
    return re.sub(" +", " ", re.compile("[^a-z0-9,.!?']").sub(" ", text.lower().strip()))


def chunk_text(text_split: list,
               chunk_size: int = 4,
               overlap_size: int = 1) -> Tuple[list, list]:
    # create next chunk by moving right pointer until chunk_size is reached or line_number changes by more than 1 or end of word_sequence is reached
    left_pointer = 0
    right_pointer = chunk_size - 1
    chunks = []
    pointers = []

    if right_pointer >= len(text_split):
        chunks = [" ".join(text_split)]
        pointers = [[0, len(text_split)]]
    else:
        while right_pointer < len(text_split):
            # check if chunk_size has been reached
            # create chunk
            chunk = text_split[left_pointer: right_pointer + 1]
            pointer_duo = [left_pointer, right_pointer]

            # move left pointer
            left_pointer += chunk_size - overlap_size

            # move right pointer
            right_pointer += chunk_size - overlap_size

            # store chunk
            chunks.append(" ".join(chunk))
            pointers.append(pointer_duo)

        # check if there is final chunk
        if len(text_split[left_pointer:]) > 0:
            last_chunk = text_split[left_pointer:]
            chunks.append(" ".join(last_chunk))
            pointers.append([left_pointer, len(text_split)])
    return chunks, pointers


def create_all(query: str,
               transcript: str) -> Tuple[list, list]:
    try:
        print("STARTING: create_all")
        text_split = clean_word(transcript).split(" ")
        query_split = query.strip().split(" ")
        query_word_length = len(query_split)
        all_chunks = []
        all_pointers = []
        for chunk_size in range(max(1, query_word_length - 1), min(len(text_split), query_word_length + 1)):
            chunks, pointers = chunk_text(text_split, chunk_size)
            all_chunks.append(chunks)
            all_pointers.append(pointers)
            
        print("SUCCESS: create_all ran successfully")
        return all_chunks, all_pointers
    except Exception as e:
        print(f"FAILURE: create_all failed with exception {e}")
        raise e