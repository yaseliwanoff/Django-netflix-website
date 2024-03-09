from django.contrib import admin
from .models import Movie, MovieList

# Регистрация модели Movies из models.py
admin.site.register(Movie)

# Регистрация модели MovieList из models.py
admin.site.register(MovieList)
