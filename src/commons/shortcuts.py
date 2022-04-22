import io

from commons.image import Image


def adjust_image(stream, format, size, quality=85):  # pylint: disable=W0622
    """
    Adjust image to save in form.
    """
    if not stream:
        # ignore if image is not valid.
        return None

    out_stream = io.BytesIO()

    Image(stream).resize(size, keep_aspect=True).save(
        out_stream, format=format, quality=quality
    )

    return out_stream
