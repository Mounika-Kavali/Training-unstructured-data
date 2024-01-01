#main.py

from dotenv import load_dotenv
import os
from PIL import Image
from combine_text import combine_text_from_pdfs
from inference import run_inference

from flask import Flask, request, jsonify
from flask_cors import CORS 

load_dotenv()

app = Flask(__name__)
CORS(app) 


pdf_folder_path = 'data/pdfs'
combined_text_path = 'data/combined.txt'

#example
# user_query = "about SAP Account"

# combine_text_from_pdfs(pdf_folder_path, combined_text_path)

# with open(combined_text_path, 'r', encoding='utf-8') as file:
#         text = file.read()

# response = run_inference(text, user_query)
# print("RESPONSE",response)


@app.route('/generate_response', methods=['POST'])
def generate_response_route():
    user_query = request.form.get('user_query')

    combine_text_from_pdfs(pdf_folder_path, combined_text_path)

    with open(combined_text_path, 'r', encoding='utf-8') as file:
        text = file.read()

    response = run_inference(text, user_query)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)

    
    




