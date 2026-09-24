from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    rate = models.FloatField()

    country = models.CharField(max_length=100, blank=True, default="")
    premiere = models.CharField(max_length=100, blank=True, default="")
    director = models.CharField(max_length=100, blank=True, default="")
    genre = models.CharField(max_length=200, blank=True, default="")
    quality = models.CharField(max_length=50, blank=True, default="")
    translation = models.CharField(max_length=200, blank=True, default="")
    age = models.CharField(max_length=10, blank=True, default="")
    duration = models.CharField(max_length=50, blank=True, default="")

    
    video = models.FileField(
        upload_to="movies/videos/",
        blank=True,
        null=True
    )

    
    image = models.ImageField(
        upload_to="movies/images/"
    )

    is_popular = models.BooleanField(default=False)

    text = models.TextField(
        max_length=1000,
        blank=True,
        default=""
    )

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Профиль {self.user.username}"


class BookmarkCategory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookmark_categories"
    )

    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    movies = models.ManyToManyField(
        Movie,
        blank=True,
        related_name="bookmark_categories"
    )

    def __str__(self):
        return self.name
    
class SavedMovie(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="saved_movies"
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="saved_by"
    )

    category = models.ForeignKey(
        BookmarkCategory,
        on_delete=models.CASCADE,
        related_name="saved_movies"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "user",
            "movie",
            "category"
        )

    def __str__(self):
        return f"{self.user.username} — {self.movie.name}"


category = models.ForeignKey(
    BookmarkCategory,
    on_delete=models.CASCADE,
    related_name="saved_movies",
    null=True,
    blank=True
)