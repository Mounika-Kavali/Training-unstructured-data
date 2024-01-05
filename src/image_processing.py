#image-processing.py

import base64
import requests
import os
from dotenv import load_dotenv

# OpenAI API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to generate text for the image and user question
def text_extraction_for_image(image_path, user_question):
    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_question
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()

# Specify the folder path containing images
image_folder = "data\imgs"
combined_text_path = 'data\combined.txt'
# Example user question
user_question = "Explain in detail about the image?"

# Iterate over each image in the folder
def generate_text_for_images():
    for image_file in os.listdir(image_folder):
        if image_file.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            image_path = os.path.join(image_folder, image_file)
            
            # Generate text for the image and user question
            response_json = text_extraction_for_image(image_path, user_question)
            print("Generated Text:", response_json['choices'][0]['message']['content'])
            response= response_json['choices'][0]['message']['content']
            with open(combined_text_path, 'a', encoding='utf-8') as file:
                file.write(response)

