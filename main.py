#main.py

from dotenv import load_dotenv
import os
from src.combine_text import combine_text_from_pdfs,combine_images_from_pdfs,combine_text_from_docx
from src.inference import run_inference
from src.image_processing import generate_text_for_images

from flask import Flask, request, jsonify
from flask_cors import CORS 
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app) 

# OpenAI API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

ALLOWED_EXTENSIONS = {'pdf', 'docx','png', 'jpg', '.jpeg'}

pdf_folder_path = 'data/pdfs'
image_folder_path = 'data/imgs'
docx_folder_path = 'data/docx'
combined_text_path = 'data'
combined_image_path = 'data/extracted_imgs'

app.config['pdf_folder_path'] = pdf_folder_path
app.config['image_folder_path'] = image_folder_path
app.config['combined_text_path'] = combined_text_path
app.config['docx_folder_path'] = docx_folder_path

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/generate_response', methods=['POST'])
def generate_response_route():
    user_query = request.form.get('user_query')
    
    if "FROM THE IMAGE" in user_query:
        return generate_text_for_images(user_query)
    else:
        pdf_images = combine_images_from_pdfs(pdf_folder_path, combined_image_path)
        print("pdf_images",pdf_images)
        with open(combined_text_path, 'r', encoding='utf-8') as file:
            text = file.read()
        response = run_inference(text, user_query)
        
        return jsonify({'response': response})


@app.route('/upload/<filename>', methods=['POST'])
def upload_file(filename):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        # Secure the filename
        filename = secure_filename(file.filename)

        if filename.endswith('.pdf'):
            file.save(os.path.join(app.config['pdf_folder_path'], filename))
             #EXTRACT TEXT FROM PDF FILE
            combine_text_from_pdfs(pdf_folder_path, combined_text_path)
             

        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            file.save(os.path.join(app.config['image_folder_path'], filename))
             
             #EXTRACT TEXT FROM IMAG FILE
            # generate_text_for_images()
            

        elif filename.endswith('.docx'):
            file.save(os.path.join(app.config['docx_folder_path'], filename))
             
            #EXTRACT TEXT FROM DOC FILE
            combine_text_from_docx(docx_folder_path, combined_text_path)
        else:
            return jsonify({'error': 'Invalid file format'})
       

        return jsonify({'fileName': filename, 'message': 'File uploaded successfully'})
    else:
        return jsonify({'error': 'Invalid file format'})
    
@app.route('/get_all_files', methods=['GET'])    
def get_all_files():
    folders = ['pdf_folder_path','image_folder_path','docx_folder_path']
    all_files = []

    for folder in folders:
        files = [file for file in os.listdir(app.config[folder])]
        all_files += files
    return jsonify({'pdfFiles':all_files})


@app.route('/remove_file/<filename>', methods=['DELETE'])
def remove_file(filename):
    pdf_path = os.path.join(app.config['pdf_folder_path'], filename)
    image_path = os.path.join(app.config['image_folder_path'], filename)
    docx_path = os.path.join(app.config['docx_folder_path'], filename)
    # Clear the content of combined.txt
    with open(combined_text_path, 'w', encoding='utf-8') as file:
        file.write('') #make combined.txt empty

    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        #EXTRACT LATEST TEXT FROM  PDF FOLDER
        combine_text_from_pdfs(pdf_folder_path, combined_text_path)
        #EXTRACT LATEST TEXT FROM IMAGE FOLDER
        generate_text_for_images()
        #EXTRACT LATEST TEXT FROM DOCX FOLDER
        combine_text_from_docx(docx_folder_path, combined_text_path)
        return jsonify({'message': f'PDF file {filename} removed successfully'})
    elif os.path.exists(image_path):
        os.remove(image_path)
         #EXTRACT LATEST TEXT FROM  PDF FOLDER
        combine_text_from_pdfs(pdf_folder_path, combined_text_path)
        #EXTRACT LATEST TEXT FROM IMAGE FOLDER
        generate_text_for_images()
        #EXTRACT LATEST TEXT FROM DOCX FOLDER
        combine_text_from_docx(docx_folder_path, combined_text_path)
        return jsonify({'message': f'Image file {filename} removed successfully'})
    elif os.path.exists(docx_path):
        os.remove(docx_path)
         #EXTRACT LATEST TEXT FROM  PDF FOLDER
        combine_text_from_pdfs(pdf_folder_path, combined_text_path)
        #EXTRACT LATEST TEXT FROM IMAGE FOLDER
        generate_text_for_images()
        #EXTRACT LATEST TEXT FROM DOCX FOLDER
        combine_text_from_docx(docx_folder_path, combined_text_path)
        return jsonify({'message': f'Image file {filename} removed successfully'})
    else:
        return jsonify({'error': f'File {filename} not found'})
    
combined_text_path = os.path.join(app.config['combined_text_path'], 'combined.txt')

    

if __name__ == '__main__':
    app.run(debug=True)

    
    