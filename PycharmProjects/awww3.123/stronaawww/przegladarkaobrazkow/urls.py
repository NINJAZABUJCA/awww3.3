from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # ex: /przegladarkaobrazkow/
    path("", views.index, name="index"),
    path("<int:SVGImage_id>/", views.wyswietlobrazek, name="detail"),
    path("edit/", login_required(views.edit), name="stronaedycji"),
    path("edit/<int:SVGImage_id>/", login_required(views.zedytujobrazek), name="edycjaobrazka")
]