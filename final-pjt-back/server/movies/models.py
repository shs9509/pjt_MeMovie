from django.db import models
from django.conf import settings
# Create your models here.

# 평점 부분 : 소수점 정리할 수 있는방법 찾기
# 날짜 부분 : 추후에 년도/월/일만 나오게 조정하기 

class TmdbMovie(models.Model):
    movie_title = models.TextField()
    original_title = models.TextField()
    overview = models.TextField()
    poster_path = models.TextField()
    genre = models.TextField()
    release_date = models.TextField()
    vote_average = models.FloatField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name= 'like_movies')

class MovieComment(models.Model):
    movie = models.ForeignKey(TmdbMovie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    rate = models.IntegerField()

class NaverMovie(models.Model):
    movie_title = models.TextField()
    original_title = models.TextField()
    overview = models.TextField()
    poster_path = models.TextField()
    genre = models.TextField()
    release_date = models.TextField()
    vote_average = models.FloatField()

class BoxofficeMovie(models.Model):
    movie_title = models.TextField()
    poster_path = models.TextField()
    show_range = models.TextField()
    rank = models.IntegerField()
    audi = models.TextField()
    sales = models.TextField()

class AgoBoxofficeMovie(models.Model):
    movie_title = models.TextField()
    poster_path = models.TextField()
    show_range = models.TextField()
    rank = models.IntegerField()
    audi = models.TextField()
    sales = models.TextField()