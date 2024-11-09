def get_purpose(textAnalyzer, text, model, temperature, max_tokens, top_p):
        """Get purpose from the given text using the Groq API."""
        completion = textAnalyzer.client.chat.completions.create(
            model=model,
            messages=[
            {"role": "user", "content": f"Text: {text}\n\nFrom the provided text, identify the 'purpose' field within the classification section"},
                {
                    "role": "system",
                    "content": """,
                    Values can be: "unspecified," "discipline," "idea," "prerequisite," "educational objective,"
                    "accessibility," "restrictions," "educational level," "skill level," "security level," and "competency."
                    Return only the purpose. If no purpose is found, respond with "No purpose"."""
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content.strip()
    
    
def get_taxon_path(textAnalyzer, text, model, temperature, max_tokens, top_p):
        """Get taxon path from the given text using the Groq API."""
        completion = textAnalyzer.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": text},
                {
                    "role": "system",
                    "content": """From the provided text, extract information related to the "Taxon Path"
                    in the classification section. The "Taxon Path" represents a hierarchical, taxonomic path
                    in a classification system where each level refines the previous one. Return only the taxon path
                    information. If no taxon path is found, respond with "No taxon path"."""
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content.strip()
    
    
def get_classification_description(textAnalyzer, text, model, temperature, max_tokens, top_p, purpose):
        """Get classification description from the given text using the Groq API."""
        
        completion = textAnalyzer.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": text},
                {
                    "role": "system",
                    "content": f"""From the provided text, extract the "Description" of the learning object relative
                    to the stated purpose ("{purpose}"). The description should explain the
                    context or details related to the stated purpose.
                    Return only the description. If no description is found, respond with "No description"."""
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content.strip()
    
    
def get_classification_keywords(textAnalyzer, text, model, temperature, max_tokens, top_p, purpose):
        """Get classification keywords from the given text using the Groq API."""
        
        completion = textAnalyzer.client.chat.completions.create(
            model=model,
            messages=[
            {"role": "user", "content": f"Text: {text}\n\nPlease extract the keywords and phrases that describe the learning object relative to the stated purpose ('{purpose}')."},
                {
                    "role": "system",
                    "content": """The keywords should be relevant to the classification purpose. Return only the keywords themselves, without any additional explanation or text before or after keywords."""
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content.strip()