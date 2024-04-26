from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
# Create your views here.
from .models import SVGImage

def index(request):
    listaobrazkow = SVGImage.objects.all()
    template = loader.get_template("przegladarkaobrazkow/index.html")
    context = {
        "listaobrazkow": listaobrazkow,
    }
    return HttpResponse(template.render(context, request))


def edit(request):
    listaobrazkow = SVGImage.objects.all()
    template = loader.get_template("przegladarkaobrazkow/edytuj.html")
    context = {
        "listaobrazkow": listaobrazkow,
    }
    return HttpResponse(template.render(context, request))

def wyswietlobrazek(request, SVGImage_id):
    template = loader.get_template("przegladarkaobrazkow/wyswietlobrazek.html")
    obrazek = SVGImage.objects.get(pk=SVGImage_id)
    svg_content = obrazek.image

    context = {
        'obrazek': obrazek,
        'svg_content': svg_content,  # Przekazanie zawartości pliku SVG do szablonu
    }
    return HttpResponse(template.render(context, request))


def is_editor(user, SVGImage_id):
    # Pobierz obiekt SVGImage
    image = get_object_or_404(SVGImage, pk=SVGImage_id)
    # Sprawdź, czy użytkownik jest edytorem tego obrazu
    return user in image.editors.all()

def zedytujobrazek(request, SVGImage_id):
    if not is_editor(request.user, SVGImage_id):
        # Jeśli użytkownik nie jest edytorem, możesz obsłużyć to tutaj,
        # na przykład przekierować na stronę błędu lub wyświetlić odpowiednią wiadomość
        return render(request, 'error.html', {'message': 'Brak dostępu.'})
    else:
        template = loader.get_template("przegladarkaobrazkow/edytujobrazek.html")
        obrazek = SVGImage.objects.get(pk=SVGImage_id)
        svg_content = obrazek.image

        context = {
            'obrazek': obrazek,
            'svg_content': svg_content,  # Przekazanie zawartości pliku SVG do szablonu
        }
        aktualna_sciezka = request.path
        if request.method == 'POST':

            if 'usun' in request.POST:
                # Dodanie nowego kształtu do zawartości pliku SVG
                obrazek.image =''

                # Zapisanie zaktualizowanej zawartości do pola image
                obrazek.save()
                return redirect(aktualna_sciezka)  # Przekierowanie na bieżącą stronę

            elif 'dodaj' in request.POST:
                # Pobranie danych z formularza
                x = request.POST.get('x')
                y = request.POST.get('y')
                width = request.POST.get('width')
                height = request.POST.get('height')
                color = request.POST.get('color')

                # Sprawdzenie, czy wszystkie pola zostały wypełnione
                if x and y and width and height and color:
                    # Odczytanie zawartości pliku SVG
                    nowy_ksztalt = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{color}"></rect>'
                    # Dodanie nowego kształtu do pliku SVG

                    # Dodanie nowego kształtu do zawartości pliku SVG
                    obrazek.image += nowy_ksztalt

                    # Zapisanie zaktualizowanej zawartości do pola image
                    obrazek.save()
                    return redirect(aktualna_sciezka)  # Przekierowanie na bieżącą stronę
                else:
                    return HttpResponseBadRequest("Proszę wypełnić wszystkie pola formularza.")

        # Renderowanie szablonu HTML
        return render(request, "przegladarkaobrazkow/edytujobrazek.html", context)
