from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from .models import BookmarkCategory, SavedMovie

from .models import (
    Movie,
    Profile,
    BookmarkCategory,
    SavedMovie,
)


def index(request):
    movies = Movie.objects.all()

    return render(
        request,
        "main/index.html",
        {
            "movies": movies
        }
    )
def catalog(request):

    movies = Movie.objects.all()

    # =========================
    # SEARCH
    # =========================

    search = request.GET.get("search", "").strip()

    if search:
        movies = movies.filter(
            name__icontains=search
        )


    # =========================
    # GENRE
    # =========================

    genre = request.GET.get("genre", "").strip()

    if genre:
        movies = movies.filter(
            genre__icontains=genre
        )


    # =========================
    # COUNTRY
    # =========================

    country = request.GET.get("country", "").strip()

    if country:
        movies = movies.filter(
            country__icontains=country
        )


    # =========================
    # YEAR
    # =========================

    year = request.GET.get("year", "").strip()

    if year:
        try:
            movies = movies.filter(
                year=int(year)
            )
        except ValueError:
            pass


    # =========================
    # MINIMUM RATING
    # =========================

    min_rating = request.GET.get("min_rating", "").strip()

    if min_rating:
        try:
            movies = movies.filter(
                rate__gte=float(min_rating)
            )
        except ValueError:
            pass


    # =========================
    # QUALITY
    # =========================

    quality = request.GET.get("quality", "").strip()

    if quality:
        movies = movies.filter(
            quality__icontains=quality
        )


    # =========================
    # SORT
    # =========================

    sort = request.GET.get("sort", "popular")

    if sort == "rating":

        movies = movies.order_by("-rate")

    elif sort == "newest":

        movies = movies.order_by("-year")

    elif sort == "oldest":

        movies = movies.order_by("year")

    elif sort == "name":

        movies = movies.order_by("name")

    else:

        movies = movies.order_by(
            "-is_popular",
            "-rate"
        )


    # =========================
    # FILTER OPTIONS
    # =========================

    genres = (
        Movie.objects
        .exclude(genre="")
        .values_list("genre", flat=True)
        .distinct()
    )

    countries = (
        Movie.objects
        .exclude(country="")
        .values_list("country", flat=True)
        .distinct()
    )

    years = (
        Movie.objects
        .values_list("year", flat=True)
        .distinct()
        .order_by("-year")
    )

    qualities = (
        Movie.objects
        .exclude(quality="")
        .values_list("quality", flat=True)
        .distinct()
    )


    return render(
        request,
        "main/catalog.html",
        {
            "movies": movies,

            "genres": genres,
            "countries": countries,
            "years": years,
            "qualities": qualities,

            "search": search,
            "selected_genre": genre,
            "selected_country": country,
            "selected_year": year,
            "selected_rating": min_rating,
            "selected_quality": quality,
            "selected_sort": sort,
        }
    )

def detail(request, id):
    movie = get_object_or_404(Movie, id=id)

    categories = []
    saved_categories = []

    if request.user.is_authenticated:

        # Все закладки пользователя
        categories = BookmarkCategory.objects.filter(
            user=request.user
        ).order_by("created_at")

        # В каких закладках уже находится этот фильм
        saved_categories = BookmarkCategory.objects.filter(
            user=request.user,
            saved_movies__movie=movie
        ).distinct()

    return render(
        request,
        "main/detail.html",
        {
            "movie": movie,
            "categories": categories,
            "saved_categories": saved_categories,
        }
    )


def register(request):

    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            return render(
                request,
                "main/register.html",
                {
                    "error": "Пароли не совпадают"
                }
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "main/register.html",
                {
                    "error": "Такой пользователь уже существует"
                }
            )

        # Создаём пользователя
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Стандартные закладки
        default_categories = [
            "Буду смотреть",
            "Уже посмотрел",
            "Не интересно",
        ]

        for category_name in default_categories:
            BookmarkCategory.objects.create(
                user=user,
                name=category_name
            )

        login(request, user)

        return redirect("profile")

    return render(
        request,
        "main/register.html"
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("profile")

        return render(
            request,
            "main/login.html",
            {
                "error": "Неверный логин или пароль"
            }
        )

    return render(
        request,
        "main/login.html"
    )


@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        if request.FILES.get("avatar"):
            profile.avatar = request.FILES["avatar"]
            profile.save()

    return render(
        request,
        "main/profile.html",
        {
            "profile": profile
        }
    )


def logout_view(request):

    logout(request)

    return redirect("index")

@login_required
def collection(request):

    categories = BookmarkCategory.objects.filter(
        user=request.user
    ).order_by("created_at")

    selected_category = None
    movies = SavedMovie.objects.none()

    category_id = request.GET.get("category")

    if category_id:

        selected_category = get_object_or_404(
            BookmarkCategory,
            id=category_id,
            user=request.user
        )

        movies = SavedMovie.objects.filter(
            user=request.user,
            category=selected_category
        ).select_related("movie", "category")

    return render(
        request,
        "main/collection.html",
        {
            "categories": categories,
            "selected_category": selected_category,
            "movies": movies,
        }
    )
@login_required
def create_category(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()

        if name:
            BookmarkCategory.objects.create(
                user=request.user,
                name=name
            )

    return redirect("collection")


@login_required
def add_movie_to_category(request, movie_id, category_id):

    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    category = get_object_or_404(
        BookmarkCategory,
        id=category_id,
        user=request.user
    )

    SavedMovie.objects.get_or_create(
        user=request.user,
        movie=movie,
        category=category
    )

    return redirect("detail", id=movie.id)
@login_required
def remove_movie_from_category(request, movie_id, category_id):

    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    category = get_object_or_404(
        BookmarkCategory,
        id=category_id,
        user=request.user
    )

    category.movies.remove(movie)

    return redirect("collection")

@login_required
@require_POST
def remove_movies_from_category(request, category_id):
    category = get_object_or_404(
        BookmarkCategory,
        id=category_id,
        user=request.user
    )

    movie_ids = request.POST.getlist('movie_ids')

    SavedMovie.objects.filter(
        user=request.user,
        category=category,
        id__in=movie_ids
    ).delete()

    return redirect(f'/collection/?category={category.id}')


@login_required
@require_POST
def delete_category(request, category_id):

    category = get_object_or_404(
        BookmarkCategory,
        id=category_id,
        user=request.user
    )

    # Удаляем все сохранённые фильмы этой закладки
    SavedMovie.objects.filter(
        category=category,
        user=request.user
    ).delete()

    # Удаляем саму закладку
    category.delete()

    return redirect("collection")