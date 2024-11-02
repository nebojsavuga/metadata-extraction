def get_title(textAnalyzer, text, model, temperature, max_tokens, top_p):
        """Get title from the given text using the Groq API."""
        completion = textAnalyzer.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": text},
                {
                    "role": "system",
                    "content": """Get the title of the text, but just title, dont add additional text"""
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
                "content": """Get very short description of the text, but just description, dont add any additional text"""
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
                "content": "Extract keywords with bullet points. Dont add any aditional text just keywords",
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


def get_structure(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get structure from the given text using the Groq API."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": text},
            {
                "role": "system",
                "content": """use just 1 word in your response and Extract structure of the text with just one of the possible values, no additional text. These are possible values: 
atomic: an object that
is indivisible (in this
context).
collection: a set of
objects with no
specified relationship
between them.
networked: a set of
objects with
relationships that are
unspecified.
hierarchical: a set of
objects whose
relationships can be
represented by a tree
structure.
linear: a set of objects
that are fully ordered.
Example: A set of
objects that are
connected by
"previous" and "next"
relationships."""
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()


def get_coverage(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get coverage from the given text using the Groq API."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": text},
            {
                "role": "system",
                "content": """use just few words in your response: Extract coverage of the text with The time, culture, geography or region to
which this learning object applies.
The extent or scope of the content of the
learning object. Coverage will typically
include spatial location (a place name or
geographic coordinates), temporal period (a
period label, date, or date range) or
jurisdiction (such as a named administrative
entity) if no coverage is found just return not found"""
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()