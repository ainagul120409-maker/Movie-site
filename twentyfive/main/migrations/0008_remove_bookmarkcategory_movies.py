from django.db import migrations


def copy_legacy_bookmarks(apps, schema_editor):
    BookmarkCategory = apps.get_model('main', 'BookmarkCategory')
    SavedMovie = apps.get_model('main', 'SavedMovie')
    database = schema_editor.connection.alias

    for category in BookmarkCategory.objects.using(database).all().iterator():
        movie_ids = category.movies.using(database).values_list('pk', flat=True)
        for movie_id in movie_ids.iterator():
            SavedMovie.objects.using(database).get_or_create(
                user_id=category.user_id,
                movie_id=movie_id,
                category_id=category.pk,
            )


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_movie_image'),
    ]

    operations = [
        migrations.RunPython(copy_legacy_bookmarks, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='bookmarkcategory',
            name='movies',
        ),
    ]
