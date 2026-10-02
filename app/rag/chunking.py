def split_text(text: str) -> list[str]:
    paragraphs = [
        paragraph.strip() for paragraph in text.split("\n") if paragraph.strip()
    ]

    chunks = []

    for index, paragraph in enumerate(paragraphs):
        chunk = paragraph

        if index > 0:
            chunk = paragraphs[index - 1] + "\n" + chunk

        if index < len(paragraphs) - 1:
            chunk = chunk + "\n" + paragraphs[index + 1]

        chunks.append(chunk)

    return chunks
