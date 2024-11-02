from groq import Groq
from metadata import *
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

        metadata_instance.general = self.get_general_data(file, text, model, temperature, max_tokens, top_p)
        metadata_instance.lifeCycle = self.get_life_cycle_data(file, text, model, temperature, max_tokens, top_p)
        metadata_instance.tehnical = self.get_tehnical_data(file, text, model, temperature, max_tokens, top_p)
        metadata_instance.educational = self.get_educational_data(file, text, model, temperature, max_tokens, top_p)
        metadata_instance.rights = self.get_rights_data(file, text, model, temperature, max_tokens, top_p)
        metadata_instance.relation = self.get_relation_data(file, text, model, temperature, max_tokens, top_p)
        metadata_instance.classification = self.get_classification_data(file, text, model, temperature, max_tokens, top_p)

        # do for others
        return metadata_instance

    def get_general_data(self, file, text, model, temperature, max_tokens, top_p):
        general = GeneralMetadata()
        general.title = self.get_title(
            text, model, temperature, max_tokens, top_p
        )
        general.keywords = self.get_keywords(
            text, model, temperature, max_tokens, top_p
        )
        general.language = self.get_language(
            text, model, temperature, max_tokens, top_p
        )
        general.aggregation_level = self.get_aggregation_level(
            text, model, temperature, max_tokens, top_p
        )
        
        return general
    
    def get_life_cycle_data(self, file, text, model, temperature, max_tokens, top_p):
        life_cycle = LifeCycleMetadata()
        # TO DO
        return life_cycle
    
    def get_tehnical_data(self, file, text, model, temperature, max_tokens, top_p):
        tehnical = TehnicalMetadata()
        # TO DO
        return tehnical
    
    def get_educational_data(self, file, text, model, temperature, max_tokens, top_p):
        educational = EducationalMetadata()
        # TO DO
        return educational
    
    def get_rights_data(self, file, text, model, temperature, max_tokens, top_p):
        rights = RightsMetadata()
        # TO DO
        return rights
    
    def get_relation_data(self, file, text, model, temperature, max_tokens, top_p):
        relation = RelationMetadata()
        # TO DO
        return relation
    
    def get_classification_data(self, file, text, model, temperature, max_tokens, top_p):
        classification = ClassificationMetadata()
        # TO DO
        return classification

    def get_title(self, text, model, temperature, max_tokens, top_p):
        """Get title from the given text using the Groq API."""
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": text},
                {
                    "role": "system",
                    "content": """Get the title of the text, but just title, without additional text"""
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content.strip()
    
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
    
    def get_language(self, text, model, temperature, max_tokens, top_p):
        """Get language from the given text using the Groq API."""
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": text},
                {
                    "role": "system",
                    "content": "Extract language of the text. Dont add any aditional text just language",
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content.strip()
    
    def get_aggregation_level(self, text, model, temperature, max_tokens, top_p):
        """Get aggregation level from the given text using the Groq API."""
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": text},
                {
                    "role": "system",
                    "content": """Extract aggregation level of the text with just level, no additional text. Aggregation level is The functional granularity of this learning object. These are possible values: 
1: the smallest level of aggregation, e.g., raw media data or fragments.
2: a collection of level 1 learning objects, e.g., a lesson.
3: a collection of level 2 learning objects, e.g., a course.
4: the largest level of granularity, e.g., a set of courses that lead to a certificate."""
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content.strip()
