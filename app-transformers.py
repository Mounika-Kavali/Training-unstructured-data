#streamlit run app-transformers.py<-----to run the file

from dotenv import load_dotenv
import os
import streamlit as st
from PyPDF2 import PdfReader
from transformers import pipeline
from PIL import Image

load_dotenv()

img = Image.open(r"C:/Users/Kavali Mounika/Pictures/Saved Pictures/neytiriii.jpg")
st.set_page_config(page_title="DocGenius: Document Generation AI", page_icon=img)
st.header("Ask Your PDF📄")
pdf = st.file_uploader("Upload your PDF", type="pdf")

if pdf is not None:
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    query = st.text_input("Ask your Question about your PDF")
    if query:
        qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", tokenizer="distilbert-base-cased-distilled-squad")

        answer = qa_pipeline({"question": query, "context": text})
        st.success(answer["answer"])
