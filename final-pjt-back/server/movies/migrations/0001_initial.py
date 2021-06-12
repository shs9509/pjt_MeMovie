# Generated by Django 3.2.3 on 2021-05-25 08:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoxofficeMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_title', models.TextField()),
                ('poster_path', models.TextField()),
                ('show_range', models.TextField()),
                ('rank', models.IntegerField()),
                ('audi', models.TextField()),
                ('sales', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='NaverMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_title', models.TextField()),
                ('original_title', models.TextField()),
                ('overview', models.TextField()),
                ('poster_path', models.TextField()),
                ('genre', models.TextField()),
                ('release_date', models.TextField()),
                ('vote_average', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RottenMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_title', models.TextField()),
                ('vote_average', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TmdbMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_title', models.TextField()),
                ('original_title', models.TextField()),
                ('overview', models.TextField()),
                ('poster_path', models.TextField()),
                ('genre', models.TextField()),
                ('release_date', models.TextField()),
                ('vote_average', models.FloatField()),
                ('like_users', models.ManyToManyField(related_name='like_movies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MovieComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('rate', models.IntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.tmdbmovie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
