#main.py

from dotenv import load_dotenv
import os
import requests
from src.combine_text import combine_text_from_pdfs,combine_images_from_pdfs
from src.inference import run_inference

from flask import Flask, request, jsonify
from flask_cors import CORS 
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app) 

# OpenAI API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', '.jpeg'}

pdf_folder_path = 'data/pdfs'
combined_text_path = 'data'
combined_image_path = 'data/extracted_imgs'
image_folder = 'data/imgs'

app.config['pdf_folder_path'] = pdf_folder_path
app.config['image_folder'] = image_folder
app.config['combined_text_path'] = combined_text_path

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/generate_response', methods=['POST'])
def generate_response_route():
    user_query = request.form.get('user_query')
    
    # Check if there are PDF files in pdf_folder_path
    pdf_files = [file for file in os.listdir(pdf_folder_path) if file.endswith('.pdf')]
    print("pdf_files in folder",pdf_files)
    if pdf_files:
         # requesting a specific uploaded file data response
        combine_text_from_pdfs(pdf_folder_path, combined_text_path)
        pdf_images = combine_images_from_pdfs(pdf_folder_path, combined_image_path)
        print("pdf_images",pdf_images)
        with open(combined_text_path, 'r', encoding='utf-8') as file:
            text = file.read()

        response = run_inference(text, user_query)
        
    else:
        # requesting a generic response
        print("user_query for chatGPT3.5",user_query)
        openai_response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            json = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_query}],
            # "temperature": 0
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
            }
        )
        response=openai_response.json()['choices'][0]['message']['content']
    
    return jsonify({'response': response})


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        # Secure the filename
        filename = secure_filename(file.filename)
        print("filename",filename)
        if filename.endswith('.pdf'):
            print("PDF")
            # Save PDF files to the specified folder
            file.save(os.path.join(app.config['pdf_folder_path'], filename))
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            # Save image files to the specified folder
            print("PNG")
            file.save(os.path.join(app.config['image_folder'], filename))
        else:
            return jsonify({'error': 'Invalid file format'})

        return jsonify({'fileName': filename, 'message': 'File uploaded successfully'})
    else:
        return jsonify({'error': 'Invalid file format'})
    
@app.route('/remove_file/<filename>', methods=['DELETE'])
def remove_file(filename):
    pdf_path = os.path.join(app.config['pdf_folder_path'], filename)
    image_path = os.path.join(app.config['image_folder'], filename)

    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        return jsonify({'message': f'PDF file {filename} removed successfully'})
    elif os.path.exists(image_path):
        os.remove(image_path)
        return jsonify({'message': f'Image file {filename} removed successfully'})
    else:
        return jsonify({'error': f'File {filename} not found'})
    
# Clear the content of combined.txt
combined_text_path = os.path.join(app.config['combined_text_path'], 'combined.txt')
with open(combined_text_path, 'w', encoding='utf-8') as file:
    file.write('empty file')  # Write an empty string


if __name__ == '__main__':
    app.run(debug=True)

    
    