def get_title(textAnalyzer, text, model, temperature, max_tokens, top_p):
        """Get title from the given text using the Groq API."""
        completion = textAnalyzer.client.chat.completions.create(
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
    
def get_description(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get description from the given text using the Groq API."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": text},
            {
                "role": "system",
                "content": """Get short description of the text, but just description, without additional text"""
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()

def get_keywords(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Generate keywords from the given text using the Groq API."""
    completion = textAnalyzer.client.chat.completions.create(
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

def get_language(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get language from the given text using the Groq API."""
    completion = textAnalyzer.client.chat.completions.create(
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

def get_aggregation_level(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get aggregation level from the given text using the Groq API."""
    completion = textAnalyzer.client.chat.completions.create(
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