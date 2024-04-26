import random
from django.core.management.base import BaseCommand
from PIL import Image as im
from PIL import ImageDraw
from stronaglownaobrazoowa.models import Tag
from stronaglownaobrazoowa.models import Image
class Command(BaseCommand):


    def handle(self, *args, **options):
        help = 'Generates and adds sample images to the database'
        # Wymiary obrazka
        width = 640
        height = 480

        # Tworzenie nowego obrazka
        image = im.new("RGB", (width, height), "white")

        # Tworzenie obiektu rysującego
        draw = ImageDraw.Draw(image)

        # Losowe rysowanie na obrazku
        for _ in range(100):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line([(x1, y1), (x2, y2)], fill="black", width=2)

        # Zapisywanie obrazka jako pliku JPG
        image_path = "images/random_image.jpg"
        image.save(image_path)

        wszystkietagi = Tag.objects.all()
        losowe_tagi = random.sample(list(wszystkietagi), 2)
        nowyobrazek = Image.objects.create(image = image_path)
        nowyobrazek.tags.add(*losowe_tagi)