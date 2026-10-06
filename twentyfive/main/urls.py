from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [

    # =========================
    # ADMIN
    # =========================

    path(
        'admin/',
        admin.site.urls
    ),
path(
    'catalog/',
    views.catalog,
    name='catalog'
),

    # =========================
    # ГЛАВНАЯ
    # =========================

    path(
        '',
        views.index,
        name='index'
    ),


    # =========================
    # ФИЛЬМ
    # =========================

    path(
        'movie/<int:id>/',
        views.detail,
        name='detail'
    ),


    # =========================
    # РЕГИСТРАЦИЯ
    # =========================

    path(
        'register/',
        views.register,
        name='register'
    ),


    # =========================
    # ВХОД
    # =========================

    path(
        'login/',
        views.login_view,
        name='login'
    ),


    # =========================
    # ПРОФИЛЬ
    # =========================

    path(
        'profile/',
        views.profile,
        name='profile'
    ),


    # =========================
    # ВЫХОД
    # =========================

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),


    # =========================
    # ЗАКЛАДКИ
    # =========================

    path(
        'collection/',
        views.collection,
        name='collection'
    ),


    # =========================
    # СОЗДАТЬ КАТЕГОРИЮ
    # =========================

    path(
        'collection/create/',
        views.create_category,
        name='create_category'
    ),


    # =========================
    # УДАЛИТЬ ФИЛЬМЫ ИЗ КАТЕГОРИИ
    # =========================

    path(
        'collection/<int:category_id>/remove/',
        views.remove_movies_from_category,
        name='remove_movies_from_category'
    ),


    # =========================
    # ДОБАВИТЬ ФИЛЬМ В КАТЕГОРИЮ
    # =========================

    path(
        'movie/<int:movie_id>/category/<int:category_id>/add/',
        views.add_movie_to_category,
        name='add_movie_to_category'
    ),


    # =========================
    # УДАЛИТЬ ФИЛЬМ ИЗ КАТЕГОРИИ
    # =========================

    path(
        'movie/<int:movie_id>/category/<int:category_id>/remove/',
        views.remove_movie_from_category,
        name='remove_movie_from_category'
    ),

    path(
    'collection/<int:category_id>/delete/',
    views.delete_category,
    name='delete_category'
),
]


# =========================
# MEDIA
# =========================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )