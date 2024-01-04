import cv2
import pytesseract


def extract_text_from_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to highlight text (adjust parameters based on your image)
    _, thresholded_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)

    # Perform OCR on the thresholded image
    extracted_text = pytesseract.image_to_string(thresholded_image)

    return extracted_text

# Example usage
image_path = 'data/imgs/Zomato-Infographic.png'
text_from_image = extract_text_from_image(image_path)

print("Extracted Text:")
print(text_from_image)

combined_text_path = 'data/combined.txt'
with open(combined_text_path, 'w', encoding='utf-8') as file:
        file.write(text_from_image)


# import os
# import io
# from PIL import Image
# import PyPDF2

# def extract_and_save_images(pdf_path, output_dir, min_width=100, min_height=100, output_format="png"):
#     # Create the output folder if it doesn't exist
#     os.makedirs(output_dir, exist_ok=True)

#     # Open the PDF file using PyPDF2
#     with open(pdf_path, "rb") as pdf_file:
#         pdf_reader = PyPDF2.PdfReader(pdf_file)
#         images_list=[]
#         # Iterate over PDF pages
#         for page_index in range(len(pdf_reader.pages)):
           
            
#             page = pdf_reader.pages[page_index]
#             print(page,"page")
            
#             # image_list = page.extract_images()
#             images_list.extend(page.get_images())
#             # Print the number of images found on this page
#             if len(images_list):
#                 print(f"[+] Found a total of {len(images_list)} images in page {page_index}")
#             else:
#                 print(f"[!] No images found on page {page_index}")

#             # Iterate over the images on the page
#             for image_index, img in enumerate(images_list, start=1):
#                 # Get the XREF of the image
#                 xref = img[0]

#                 # Extract the image bytes
#                 base_image = pdf_reader.extract_image(xref)
#                 image_bytes = base_image["image"]

#                 # Get the image extension
#                 image_ext = base_image["ext"]

#                 # Load it to PIL
#                 image = Image.open(io.BytesIO(image_bytes))

#                 # Check if the image meets the minimum dimensions and save it
#                 if image.width >= min_width and image.height >= min_height:
#                     image.save(
#                         open(os.path.join(output_dir, f"image{page_index + 1}_{image_index}.{output_format}"), "wb"),
#                         format=output_format.upper())
#                 else:
#                     print(f"[-] Skipping image {image_index} on page {page_index} due to its small size.")

# if __name__ == "__main__":
#     # Input PDF file path
#     pdf_path = 'data/pdfs/sap-accounts-payable.pdf'
#     output_folder_path = 'data/extracted_images'

#     extract_and_save_images(pdf_path, output_folder_path)
