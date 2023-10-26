import uuid
from io import BytesIO

from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models


# Not used atm
class ResizeImageMixin:
    def resize(self, image_field: models.ImageField, size: tuple):
        im = Image.open(image_field)  # Catch original
        source_image = im.convert('RGB')
        source_image.thumbnail(size)  # Resize to size
        output = BytesIO()
        source_image.save(output, format='JPEG')  # Save resize image to bytes
        output.seek(0)

        content_file = ContentFile(output.read())  # Read output and create ContentFile in memory
        file = File(content_file)

        random_name = f'{uuid.uuid4()}.jpeg'
        image_field.save(random_name, file, save=False)
