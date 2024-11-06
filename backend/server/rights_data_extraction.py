def get_cost(textAnalyzer, text, model, temperature, max_tokens, top_p):
        """Get Cost from the given text using the Groq API."""
        completion = textAnalyzer.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": text},
                {
                    "role": "system",
                    "content": """Does use of this learning object requires payment answer in 1 word, yes or no"""
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content.strip()
    
    
def get_copyright(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get copyright from the given text using the Groq API."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": text},
            {
                "role": "system",
                "content": """Does copyright or other restrictions apply
to the use of this learning object. answer in 1 word, yes or no"""
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()


def get_rights_description(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Generate rights description from the given text using the Groq API."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": text},
            {
                "role": "system",
                "content": """Comments just on the conditions of use of this learning object dont talk about anything else. Example : Use of this learning object is only
permitted after a donation has been made to
Amnesty International.")""",
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()