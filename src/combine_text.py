#combine_text.py

import os
from src.preprocessing import extract_text_from_pdf,extract_images_from_pdf,extract_text_from_docx

def combine_text_from_pdfs(pdf_folder, combined_text_path):
    pdf_texts = [extract_text_from_pdf(os.path.join(pdf_folder, pdf_file)) 
    for pdf_file in os.listdir(pdf_folder)]
    combined_text = "\n".join(pdf_texts)

    with open(combined_text_path, 'a', encoding='utf-8') as file:
        file.write(combined_text)

def combine_text_from_docx(docx_folder, combined_text_path):
    for file_name in os.listdir(docx_folder):
        file_path = os.path.join(docx_folder, file_name)

        if file_name.lower().endswith('.docx'):
            text, tables = extract_text_from_docx(file_path)
            
            # Process and use text and tables as needed
            combined_text = f"Docx Text:\n{text}\n\nDocx Tables:\n{tables}"
            
            with open(combined_text_path, 'a', encoding='utf-8') as file:
                file.write(combined_text)


def combine_images_from_pdfs(pdf_folder, image_folder):
    pdf_images = []

    for pdf_file in os.listdir(pdf_folder):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        images = extract_images_from_pdf(pdf_path, image_folder)
        pdf_images.extend(images)

    return pdf_images
