from transformers import ViTFeatureExtractor, VisionEncoderDecoderModel, ViTForImageClassification
import cv2

def extract_text_from_image_vit(image_path):
    # Load the ViT model and feature extractor
    model_name = "google/vit-base-patch16-224-in21k"
    feature_extractor = ViTFeatureExtractor.from_pretrained(model_name)
    model = ViTForImageClassification.from_pretrained(model_name)

    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Resize the image to the model's expected size
    resized_image = cv2.resize(image, (224, 224))

    # Convert the image to RGB format (transformers expects RGB)
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

    # Extract features from the image using the feature extractor
    inputs = feature_extractor(images=rgb_image, return_tensors="pt")
    outputs = model(**inputs)

    # Get the predicted token IDs
    predicted_ids = outputs.logits.argmax(-1)

    # Decode the predicted token IDs to text
    extracted_text = feature_extractor.decode(predicted_ids[0])

    return extracted_text

# Example usage
image_path = 'data/imgs/Zomato-Infographic.png'
text_from_image_vit = extract_text_from_image_vit(image_path)

print("Extracted Text from ViT:")
print(text_from_image_vit)

# Save the extracted text to a file
combined_text_path_vit = 'data/combined_vit.txt'
with open(combined_text_path_vit, 'w', encoding='utf-8') as file:
    file.write(text_from_image_vit)
