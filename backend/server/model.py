from groq import Groq
from metadata import Metadata
import os
import PyPDF2
import docx
from flask import jsonify


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()


def extract_text_from_word(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()


class TextAnalyzer:
    def __init__(self, api_key=None):
        self.client = Groq(api_key=api_key or os.environ.get("GROQ_API_KEY"))

    def get_metadata(
        self, file, model="llama3-70b-8192", temperature=0.5, max_tokens=1000, top_p=1
    ):

        text = ""
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif file.filename.endswith(".docx"):
            text = extract_text_from_word(file)
        elif file.filename.endswith(".mp3"):
            return (
                jsonify({"error": "MP3 file type not supported for text extraction"}),
                400,
            )
        else:
            return jsonify({"error": "Unsupported file type"}), 400
        if not text:
            return jsonify({"error": "Could not extract text from the file"}), 400

        metadata_instance = Metadata()
        metadata_instance.general.keywords = self.get_keywords(
            text, model, temperature, max_tokens, top_p
        )
        return metadata_instance

    def get_keywords(self, text, model, temperature, max_tokens, top_p):
        """Generate keywords from the given text using the Groq API."""
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": text},
                {
                    "role": "system",
                    "content": "Extract keywords with bullet points. Dont add any aditional text",
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content.strip()
