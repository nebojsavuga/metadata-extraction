from groq import Groq
from general_data_extraction import *
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
        general.title = get_title(
            self, text, model, temperature, max_tokens, top_p
        )
        general.description = get_description(
            self, text, model, temperature, max_tokens, top_p
        )
        general.keywords = get_keywords(
            self, text, model, temperature, max_tokens, top_p
        )
        general.language = get_language(
            self, text, model, temperature, max_tokens, top_p
        )
        general.aggregation_level = get_aggregation_level(
            self, text, model, 0.1, max_tokens, top_p
        )
        general.structure = get_structure(
            self, text, model, temperature, max_tokens, top_p
        )
        general.coverage = get_coverage(
            self, text, model, temperature, max_tokens, top_p
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

    
