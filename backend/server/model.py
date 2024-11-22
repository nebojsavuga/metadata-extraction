from groq import Groq
from general_data_extraction import *
from technical_data_extraction import *
from rights_data_extraction import *
from educational_data_extraction import *
from life_cycle_data_extraction import *
from classification_data_extraction import *
from sql_service import *
from metadata import *
import os
from flask import jsonify
import re
import tiktoken
from concurrent.futures import ThreadPoolExecutor
from text_extractors import *
# Supported video and audio formats
VIDEO_FORMATS = ["mp4", "mkv", "avi", "mov"]
AUDIO_FORMATS = ["mp3", "wav", "aac", "flac"]


def split_text_by_word_count(text, word_limit=2000):
    words = re.split(r"(\s+)", text)
    segments = []
    current_segment = []
    current_word_count = 0

    for word in words:
        current_segment.append(word)
        if word.strip():
            current_word_count += 1

        if current_word_count >= word_limit:
            segments.append("".join(current_segment).strip())
            current_segment = []
            current_word_count = 0

    if current_segment:
        segments.append("".join(current_segment).strip())

    return segments


class TextAnalyzer:
    def __init__(self, api_key=None):
        self.client = Groq(api_key=api_key or os.environ.get("GROQ_API_KEY"))
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def get_metadata(
        self, file, model="llama3-8b-8192", temperature=0.5, max_tokens=1000, top_p=1
    ):

        text = ""
        if file.filename.endswith(".pdf"):
            text = extract_pdf(file)
        elif file.filename.endswith(".docx"):
            text = extract_word(file)
        elif file.filename.endswith(".pptx"):
            text = extract_pptx(file)
        else:
            text = "No data."
        if not text:
            return jsonify({"error": "Could not extract text from the file"}), 400
        num_tokens = len(self.tokenizer.encode(text))
        if num_tokens > 5000:
            words = split_text_by_word_count(text)
            short_text = []
            for word in words:
                completion = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": word},
                        {
                            "role": "system",
                            "content": """Get description of the text, but just description, dont add any additional text""",
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
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(
                    self.get_general_data,
                    file,
                    text,
                    model,
                    temperature,
                    max_tokens,
                    top_p,
                ): "general",
                executor.submit(
                    self.get_life_cycle_data,
                    file,
                    text,
                    model,
                    temperature,
                    max_tokens,
                    top_p,
                ): "lifeCycle",
                executor.submit(
                    self.get_tehnical_data,
                    file,
                    text,
                    model,
                    temperature,
                    max_tokens,
                    top_p,
                ): "tehnical",
                executor.submit(
                    self.get_educational_data,
                    file,
                    text,
                    model,
                    temperature,
                    max_tokens,
                    top_p,
                ): "educational",
                executor.submit(
                    self.get_rights_data,
                    file,
                    text,
                    model,
                    temperature,
                    max_tokens,
                    top_p,
                ): "rights",
                executor.submit(
                    self.get_relation_data,
                    file,
                    text,
                    model,
                    temperature,
                    max_tokens,
                    top_p,
                ): "relation",
                executor.submit(
                    self.get_classification_data,
                    file,
                    text,
                    model,
                    temperature,
                    max_tokens,
                    top_p,
                ): "classification",
            }

            for future in futures:
                section_name = futures[future]
                try:
                    setattr(metadata_instance, section_name, future.result())
                except Exception as e:
                    print(f"Error processing {section_name}: {e}")
        insert_general_metadata(file.filename, metadata_instance, 'db_config.json')
        return metadata_instance
    

    def get_general_data(self, file, text, model, temperature, max_tokens, top_p):
        general = GeneralMetadata()

        general.title = get_title(self, text, model, temperature, max_tokens, top_p)

        general.description = get_educational_description(
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
        life_cycle.version = get_version(
            self, text, model, temperature, max_tokens, top_p
        )
        life_cycle.contribute = get_contribute(
            self, text, model, 0.1, max_tokens, top_p
        )
        return life_cycle

    def get_tehnical_data(self, file, text, model, temperature, max_tokens, top_p):
        tehnical = TehnicalMetadata()
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
        educational.interactivity_type = get_interactivity_type(
            self, text, model, 0.1, max_tokens, top_p
        )
        educational.interactivity_level = get_interactivity_level(
            self, text, model, 0.1, max_tokens, top_p
        )
        educational.learning_resource_type = get_learning_resource_type(
            self, text, model, 0.1, max_tokens, top_p
        )
        educational.semantic_density = get_semantic_density(
            self, text, model, 0.1, max_tokens, top_p
        )
        educational.intended_end_user_role = get_intended_user_role(
            self, text, model, 0.1, max_tokens, top_p
        )
        educational.context = get_educational_context(
            self, text, model, 0.1, max_tokens, top_p
        )
        educational.typical_age_range = get_typical_age_range(
            self, text, model, 0.1, max_tokens, top_p
        )
        educational.difficulty = get_dificulty(
            self,
            text,
            educational.intended_end_user_role,
            model,
            0.1,
            max_tokens,
            top_p,
        )
        educational.typical_learning_time = get_learning_time(
            self,
            text,
            educational.context,
            educational.typical_age_range,
            model,
            0.1,
            max_tokens,
            top_p,
        )
        educational.description = get_educational_description(
            self, text, model, 0.1, max_tokens, top_p
        )
        return educational

    def get_rights_data(self, file, text, model, temperature, max_tokens, top_p):
        rights = RightsMetadata()
        rights.cost = get_cost(self, text, model, 0.1, max_tokens, top_p)
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
        classification.purpose = get_purpose(
            self, text, model, temperature, max_tokens, top_p
        )
        classification.taxon_path = get_taxon_path(
            self, text, model, temperature, max_tokens, top_p
        )
        classification.description = get_classification_description(
            self, text, model, temperature, max_tokens, top_p, classification.purpose
        )
        classification.keywords = get_classification_keywords(
            self, text, model, temperature, max_tokens, top_p, classification.purpose
        )
        return classification
