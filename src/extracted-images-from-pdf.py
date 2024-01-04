import fitz  # PyMuPDF
import os

def extract_images_from_pdf(pdf_path, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    for page_number in range(pdf_document.page_count):
        # Get the page
        page = pdf_document[page_number]
        # Get the images on the page
        images = page.get_images(full=True)

        for img_index, image in enumerate(images):
            image_index = image[0]
            base_image = pdf_document.extract_image(image_index)

            # Get image information
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"page{page_number + 1}_img{img_index + 1}.{image_ext}"

            # Save the image to the output folder
            image_path = os.path.join(output_folder, image_filename)
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

    # Close the PDF file
    pdf_document.close()

if __name__ == "__main__":
    # Input PDF file path
    pdf_file_path = "data/pdfs/sap-accounts-payable.pdf"

    # Output folder for extracted images
    output_folder_path = "data/extracted-images"

    # Extract images from the PDF and save them to the output folder
    extract_images_from_pdf(pdf_file_path, output_folder_path)