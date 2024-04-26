from django.urls import path
from . import views


urlpatterns = [
    # ex: /przegladarkaobrazkow/
    path("", views.index, name="index"),
    path("<int:Image_id>/", views.stronaobrazka, name="detail"),
]