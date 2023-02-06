from django.core.exceptions import ValidationError


def validate_image_size(image):
    max_size_kb = 500

    if image.size > max_size_kb * 1024:
        raise ValidationError(f'Images cannot be larger than {max_size_kb}KB!')