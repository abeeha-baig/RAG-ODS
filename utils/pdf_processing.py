from PyPDF2 import PdfReader
import re
import os

def load_and_process_pdfs(pdf_paths, pdf_sources):
    """
    Load and process PDFs, extracting text and chunking it by title with metadata.
    """
    from .chunking import chunk_by_title
    all_chunks = []

    for pdf_path in pdf_paths:
        raw_text = ""
        pdf_reader = PdfReader(pdf_path)
        for page in pdf_reader.pages:
            raw_text += page.extract_text() or ""

        raw_text = remove_text_before_second_preface(raw_text)
        source_url = pdf_sources.get(os.path.basename(pdf_path), "Source not available")
        chunks = chunk_by_title(raw_text, source_url)
        
        all_chunks.extend(chunks)
    return all_chunks

def remove_text_before_second_preface(text):
    """
    Remove text before the second occurrence of the word 'Preface'.
    """
    occurrences = [m.start() for m in re.finditer(r'\bPreface\b', text)]
    if len(occurrences) >= 2:
        start_pos = occurrences[1]
        return text[start_pos:]
    else:
        return text