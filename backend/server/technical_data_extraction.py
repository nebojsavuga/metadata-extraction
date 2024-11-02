def get_format(file):
    """Get format of the file. Example pdf,mp4."""
    file_name_data = file.filename.split('.')
    return file_name_data[len(file_name_data) - 1]