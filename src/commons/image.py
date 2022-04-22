import base64
import io

from PIL import Image as PILImage


class Image:
    def __init__(self, path_or_stream):
        self._image = PILImage.open(path_or_stream)

    def resize(self, size, keep_aspect=True):
        """
        Resize image.

        Args:
            size (tuple(width, height), required) - new image size.
            keep_aspect (bool, optional) - define whether the original aspect will be kept.
        """
        width, height = size

        if keep_aspect:
            aspect = self._image.width / self._image.height

            if self._image.width > width:
                # resize based on width.
                self._image = self._image.resize(
                    (width, int(width / aspect)), PILImage.ANTIALIAS
                )

            elif self._image.height > height:
                # resize based on height.
                self._image = self._image.resize(
                    (int(height * aspect), height), PILImage.ANTIALIAS
                )

        return self

    def _enforce_white_background(self, image):  # noqa
        """
        Enforce white background to image.
        """
        if image.mode == "LA":
            # convert to rgba to add white background.
            image = image.convert("RGBA")

        if image.mode == "RGBA":
            background = PILImage.new("RGBA", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background.convert("RGB")

        return image

    def to_webp(self, output, quality=100):
        """Converts image to WEBP."""
        image = self._enforce_white_background(self._image.copy())
        image.save(output, format="webp", quality=quality)

    def to_jpeg(self, output, quality=100):
        """Converts image to JPEG."""
        image = self._enforce_white_background(self._image.copy())
        image.save(output, format="jpeg", quality=quality)

    def to_base64(self):
        """
        Convert image file to base64.
        """
        buffer = io.BytesIO()
        self.save(buffer)
        buffer.seek(0)

        # convert content to base64
        content = base64.b64encode(buffer.read()).decode("utf-8")

        # convert file to base64
        return f"data:image/{self._image.format.lower()};base64,{content}"

    def to_gray_scale(self):
        """Convert image to gray scale."""
        self._image = self._image.convert("L")
        return self

    def save(self, output, format=None, quality=100):  # noqa
        image = self._image.copy()

        if format == "JPEG":
            self.to_jpeg(output, quality=quality)

        elif format == "WEBP":
            self.to_webp(output, quality=quality)

        else:
            image.save(output, format=format, quality=quality)

    @classmethod
    def from_base64(cls, content):
        """
        Convert a base64 content to a stream file.
        """
        buffer = io.BytesIO(base64.b64decode(content))
        return Image(buffer)
