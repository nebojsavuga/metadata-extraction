from metadata import *
import PyPDF2
import docx
from PIL import Image
import io
import fitz
from transformers import BlipProcessor, BlipForConditionalGeneration
import pptx

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

def generate_caption(image: Image.Image) -> str:
    """Generate a caption for an image using a pre-trained model."""
    inputs = processor(image, return_tensors="pt")
    output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption


def extract_word(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    image_captions = []
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            image_data = rel.target_part.blob
            image = Image.open(io.BytesIO(image_data))

            caption = generate_caption(image)
            image_captions.append(caption)

    if len(image_captions) > 1:
        image_captions = image_captions[::-1]
    combined_output = text
    for caption in image_captions:
        combined_output += f"\nImage caption: {caption}"

    return combined_output


def extract_pdf(file):
    text_output = ""
    reader = PyPDF2.PdfReader(file)
    file.seek(0)
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")

    for page_index in range(len(pdf_document)):
        text_output += reader.pages[page_index].extract_text() + "\n"

        page = pdf_document.load_page(page_index)
        image_list = page.get_images(full=True)

        for _, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]

            image = Image.open(io.BytesIO(image_bytes))
            caption = generate_caption(image)
            text_output += "Image caption: " + caption + "\n"
    return text_output.strip()