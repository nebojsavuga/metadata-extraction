import os


def get_file_format(file):
    """Get format of the file. Example pdf,mp4."""
    file_name_data = file.filename.split(".")
    return file_name_data[len(file_name_data) - 1]


def get_file_size(file):
    """Get size of file in bytes."""
    file.seek(0, os.SEEK_END)
    file_size_mb = file.tell()
    file.seek(0)
    return file_size_mb


def get_location(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get location from the file."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": text},
            {
                "role": "system",
                "content": """Return guessed geographical location without any explanation. If no location is found return Not Found.""",
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()
