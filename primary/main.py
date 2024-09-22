import pypdf
import fitz  # pip install pymupdf
import os

# extract text from pdf using pypdf
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# extract images from pdf using pymupdf (fitz)
def extract_images_from_pdf(pdf_path, output_folder="images"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    doc = fitz.open(pdf_path)
    image_files = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # load each page
        images = page.get_images(full=True)  # get all images on the page

        for img_index, img in enumerate(images):
            xref = img[0]  # xref is reference number for image
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = os.path.join(output_folder, f"page_{page_num+1}_image_{img_index+1}.{image_ext}")

            # write extracted image to output folder
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            image_files.append(image_path)

    return image_files

# set path
pdf_path = "sample.pdf"

# extract text
text = extract_text_from_pdf(pdf_path)
print("Extracted Text:\n", text)

# extract images to \images folder
image_files = extract_images_from_pdf(pdf_path)
print("Extracted Images:", image_files)
