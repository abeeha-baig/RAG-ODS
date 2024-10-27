import re
import uuid

def is_title(line):
    """
    Check if a line represents a title based on its format.
    """
    return re.match(r'^\d+(\.\d+)*\s+.*', line.strip()) is not None

def chunk_by_title(text, source_url, min_chunk_size=200, max_chunk_size=3500):
    """
    Chunk the text into segments based on titles, ensuring chunks are within the specified size limits.
    Generate metadata for each chunk including a unique ID.
    """
    lines = text.splitlines()
    chunks = []
    current_chunk = []
    current_chunk_size = 0

    for line in lines:
        if is_title(line):
            if current_chunk:
                if current_chunk_size >= min_chunk_size:
                    chunk_text = "\n".join(current_chunk).strip()
                    chunk_id = str(uuid.uuid4())
                    metadata = {
                        'id': chunk_id,
                        'source': source_url,
                        'length': current_chunk_size
                    }
                    chunks.append((chunk_text, metadata))
                current_chunk = []
                current_chunk_size = 0
            current_chunk.append(line)
            current_chunk_size += len(line)
        else:
            current_chunk.append(line)
            current_chunk_size += len(line)

        if current_chunk_size >= max_chunk_size:
            chunk_text = "\n".join(current_chunk).strip()
            chunk_id = str(uuid.uuid4())
            metadata = {
                'id': chunk_id,
                'source': source_url,
                'length': current_chunk_size
            }
            chunks.append((chunk_text, metadata))
            current_chunk = []
            current_chunk_size = 0

    if current_chunk:
        chunk_text = "\n".join(current_chunk).strip()
        chunk_id = str(uuid.uuid4())
        metadata = {
            'id': chunk_id,
            'source': source_url,
            'length': current_chunk_size
        }
        chunks.append((chunk_text, metadata))

    return chunks