import openai
import requests
import base64

# Set your OpenAI API key
openai.api_key = "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"

def encode_file(file_path):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')

def generate_text_with_file(file_path, user_question):
    base64_file = encode_file(file_path)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_question},
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "assistant",
                "content": "Here is some information:",
                "file": {"data": f"data:application/pdf;base64,{base64_file}"},
            },
        ],
        max_tokens=150,
    )

    return response.choices[0].message.content

# Example usage
file_path = "data/pdfs/Amazon-note.pdf"
user_question = "What information does this file contain?"

generated_text = generate_text_with_file(file_path, user_question)
print("Generated Text:", generated_text)
