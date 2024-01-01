#combine_text.py

import os
from preprocessing import extract_text_from_pdf

def combine_text_from_pdfs(pdf_folder, combined_text_path):
    pdf_texts = [extract_text_from_pdf(os.path.join(pdf_folder, pdf_file)) for pdf_file in os.listdir(pdf_folder)]
    combined_text = "\n".join(pdf_texts)

    with open(combined_text_path, 'w', encoding='utf-8') as file:
        file.write(combined_text)

