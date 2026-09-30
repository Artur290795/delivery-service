def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:

    text_size = len(text)
    
    if text_size < chunk_size:
        return [text]
    result = []
    step = chunk_size - overlap

    for start in range(0, text_size, step):
        end = start + chunk_size
        result.append(text[start:end])

    return result