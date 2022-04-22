from io import BytesIO

from PIL import Image
from faker.providers import BaseProvider


class Provider(BaseProvider):
    def image(self):
        """
        Creates a sample stream file to send into test.
        """
        stream = BytesIO()
        Image.new("RGBA", size=(50, 50), color=(0, 0, 0)).save(stream, "png")

        stream.name = self.generator.file_name(extension="png")
        stream.seek(0)

        return stream
