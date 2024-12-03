import os
from moviepy.editor import VideoFileClip, AudioFileClip
import tempfile


def get_file_format(file):
    """Get format of the file. Example pdf,mp4."""
    file_name_data = file.filename.split(".")
    return file_name_data[len(file_name_data) - 1]


def get_file_size(file):
    """Get size of file in bytes."""
    
    file.seek(0, os.SEEK_END)
    file_size_mb = file.tell()
    file.seek(0)
    return str(file_size_mb/1000000)


def get_location(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get location from the file."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": text},
            {
                "role": "system",
                "content": """Return guessed geographical location without any explanation. If no location is found return Not Found.""",
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()


def get_requirement(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get requirement for materials if any."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": text},
            {
                "role": "system",
                "content": """Return installation or usage requirements as bullet points if any are given in the file.  If not return No requirements found.""",
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()


def get_installation_remarks(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get requirement for materials if any."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": text},
            {
                "role": "system",
                "content": """Return installation or usage remarks as bullet points if any are given in the file.  If not return No remarks found.""",
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()


def get_duration(file, file_format, video_formats, audio_formats):
    """Get duration of the audio/video in seconds."""
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, f"temp_file{file_format}")

    try:
        file.save(temp_file_path)

        # Select the appropriate clip based on format
        if file_format in video_formats:
            clip = VideoFileClip(temp_file_path)
        elif file_format in audio_formats:
            clip = AudioFileClip(temp_file_path)
        else:
            return None

        duration = clip.duration
        clip.close()

        return duration

    except Exception as e:
        print(f"Error retrieving duration: {e}")
        return None

    finally:
        # cleanup
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
