from django.contrib import admin
from .models import Tag
from .models import Image
# Register your models here.
admin.site.register(Tag)
admin.site.register(Image)