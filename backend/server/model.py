from groq import Groq
from general_data_extraction import *
from technical_data_extraction import *
from rights_data_extraction import *
from metadata import *
import os
import PyPDF2
import docx
from flask import jsonify
import re
import tiktoken
# Supported video and audio formats
VIDEO_FORMATS = ["mp4", "mkv", "avi", "mov"]
AUDIO_FORMATS = ["mp3", "wav", "aac", "flac"]


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


def split_text_by_word_count(text, word_limit=2000):
    words = re.split(r'(\s+)', text)
    segments = []
    current_segment = []
    current_word_count = 0

    for word in words:
        current_segment.append(word)
        if word.strip(): 
            current_word_count += 1

        if current_word_count >= word_limit:
            segments.append(''.join(current_segment).strip())
            current_segment = []
            current_word_count = 0

    if current_segment:
        segments.append(''.join(current_segment).strip())

    return segments

class TextAnalyzer:
    def __init__(self, api_key=None):
        self.client = Groq(api_key=api_key or os.environ.get("GROQ_API_KEY"))
        self.tokenizer = tiktoken.get_encoding("cl100k_base")  
    def get_metadata(
        self, file, model="llama3-70b-8192", temperature=0.5, max_tokens=1000, top_p=1
    ):
        
        text = ""
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif file.filename.endswith(".docx"):
            text = extract_text_from_word(file)
        else:
            text = "No data."
        if not text:
            return jsonify({"error": "Could not extract text from the file"}), 400
        num_tokens = len(self.tokenizer.encode(text))
        if (num_tokens > 5000):
            words = split_text_by_word_count(text)
            short_text = []
            for word in words:
                completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": word},
                    {
                        "role": "system",
                        "content": """Get description of the text, but just description, dont add any additional text"""
                    },
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stream=False,
            )
                short_text.append(completion.choices[0].message.content.strip())
            text = "".join(short_text)
                
        metadata_instance = Metadata()

        metadata_instance.general = self.get_general_data(
            file, text, model, temperature, max_tokens, top_p
        )
        metadata_instance.lifeCycle = self.get_life_cycle_data(
            file, text, model, temperature, max_tokens, top_p
        )
        metadata_instance.tehnical = self.get_tehnical_data(
            file, text, model, temperature, max_tokens, top_p
        )
        metadata_instance.educational = self.get_educational_data(
            file, text, model, temperature, max_tokens, top_p
        )
        metadata_instance.rights = self.get_rights_data(
            file, text, model, temperature, max_tokens, top_p
        )
        metadata_instance.relation = self.get_relation_data(
            file, text, model, temperature, max_tokens, top_p
        )
        metadata_instance.classification = self.get_classification_data(
            file, text, model, temperature, max_tokens, top_p
        )

        return metadata_instance

    def get_general_data(self, file, text, model, temperature, max_tokens, top_p):
        general = GeneralMetadata()
        
        general.title = get_title(self, text, model, temperature, max_tokens, top_p)
        
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
        # TODO
        return life_cycle

    def get_tehnical_data(self, file, text, model, temperature, max_tokens, top_p):
        tehnical = TehnicalMetadata()
        # TODO Other platform requirements check with professor
        tehnical.format = get_file_format(file)

        tehnical.size = get_file_size(file)

        tehnical.location = get_location(
            self, text, model, temperature, max_tokens, top_p
        )
        tehnical.requirement = get_requirement(
            self, text, model, temperature, max_tokens, top_p
        )
        tehnical.installation_remarks = get_installation_remarks(
            self, text, model, temperature, max_tokens, top_p
        )
        if tehnical.format in VIDEO_FORMATS + AUDIO_FORMATS:
            tehnical.duration = get_duration(
                file, tehnical.format, VIDEO_FORMATS, AUDIO_FORMATS
            )

        return tehnical

    def get_educational_data(self, file, text, model, temperature, max_tokens, top_p):
        educational = EducationalMetadata()
        # TODO
        return educational

    def get_rights_data(self, file, text, model, temperature, max_tokens, top_p):
        rights = RightsMetadata()
        rights.cost = get_cost(
            self, text, model, 0.1, max_tokens, top_p
        )
        rights.copyright = get_copyright(
            self, text, model, temperature, max_tokens, top_p
        )
        rights.description = get_rights_description(
            self, text, model, temperature, max_tokens, top_p
        )
        return rights

    def get_relation_data(self, file, text, model, temperature, max_tokens, top_p):
        relation = RelationMetadata()
        # TODO
        return relation

    def get_classification_data(
        self, file, text, model, temperature, max_tokens, top_p
    ):
        classification = ClassificationMetadata()
        # TODO
        return classification
