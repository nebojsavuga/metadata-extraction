from groq import Groq
from metadata import Metadata
import os

class TextAnalyzer:
    def __init__(self, api_key=None):
        self.client = Groq(
            api_key=api_key or os.environ.get("GROQ_API_KEY")
        )

    def get_metadata(self, text = '', model="llama3-70b-8192", temperature=0.5, max_tokens=1000, top_p=1):
        metadata_instance = Metadata()
        metadata_instance.general.keywords = self.get_keywords(text, model, temperature, max_tokens, top_p)
        return metadata_instance
    
    def get_keywords(self, text, model, temperature, max_tokens, top_p):
        """Generate keywords from the given text using the Groq API."""
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": text},
                {"role": "system", "content": 'Extract keywords with bullet points. Dont add any aditional text'}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content.strip()
