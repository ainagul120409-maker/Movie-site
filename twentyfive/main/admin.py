from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'year',
        'rate',
        'genre',
        'is_popular',
    )

    list_filter = (
        'year',
        'genre',
        'is_popular',
    )

    search_fields = (
        'name',
        'director',
        'genre',
    )