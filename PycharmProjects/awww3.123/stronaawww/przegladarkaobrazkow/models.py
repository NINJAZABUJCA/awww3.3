from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
def validate_positive(value):
    if value <= 0:
        raise ValidationError('Wartość musi być większa niż zero.')

def default_svg_content():
    return ''

class SVGImage(models.Model):
    editors = models.ManyToManyField(User, related_name='editable_images', blank = True)
    image = models.TextField(default=default_svg_content, blank = True)
    name = models.CharField(max_length=100)
    width = models.IntegerField(validators=[validate_positive])
    height = models.IntegerField(validators=[validate_positive])
# Create your models here.
