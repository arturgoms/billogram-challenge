import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def _get_file(path_or_stream, filename=None):
    """
    Get a file instance from filesystem or stream.

    Args:
        path_or_stream (Union[str, File], required): File.
        filename (str, optional): Filename.

    Returns:
        django.core.files.base.ContentFile
    """
    if isinstance(path_or_stream, str):
        with open(path_or_stream, "rb") as f:
            return ContentFile(
                f.read(), name=filename or os.path.split(path_or_stream)[1]
            )

    return ContentFile(path_or_stream.read(), name=filename or path_or_stream.name)


def upload_file(path_or_stream, upload_path, filename=None, storage=None):
    """
    Upload a file a given storage.

    Args:
        path_or_stream (Union[str, File], required): File to upload.
        upload_path (Union[str, Callable], required): Path to upload the file.
        filename (str, optional): Filename.
        storage (django.core.files.storage.Storage, optional): Storage to perform upload.
            Default: django.core.files.storage.DefaultStorage

    Returns:
        str
    """
    storage = storage or default_storage
    file = _get_file(path_or_stream, filename=filename)
    name = (
        upload_path(file.name)
        if callable(upload_path)
        else os.path.join(upload_path, file.name)
    )
    return storage.save(name=name, content=file)
