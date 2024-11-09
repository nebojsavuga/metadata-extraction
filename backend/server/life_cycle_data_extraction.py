def get_version(textAnalyzer, text, model, temperature, max_tokens, top_p):
        """Get version from the given text using the Groq API."""
        completion = textAnalyzer.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": text},
                {
                    "role": "system",
                    "content": """From the given text content, identify and extract only the version information.
                    Return only the version. If no version is found, respond with "No version."""
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content.strip()
    
def get_contribute(textAnalyzer, text, model, temperature, max_tokens, top_p):
        """Get contribute from the given text using the Groq API."""
        completion = textAnalyzer.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": text},
                {
                    "role": "system",
                    "content": """Extract the names of all
                    contributors (i.e., people or organizations) who have played
                    a role in the life cycle of this learning object (e.g., creation, editing, publication)
                    from the provided text. Only return the list of contributors. If no contributors are found,
                    respond with "No contributors."""
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content.strip()