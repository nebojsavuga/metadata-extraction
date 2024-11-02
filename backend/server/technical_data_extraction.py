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
