from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import MovieComment, TmdbMovie, BoxofficeMovie, NaverMovie,AgoBoxofficeMovie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmdbMovie
        fields = '__all__'

class MovieCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieComment
        fields = '__all__'
        read_only_fields = ('movie',) # 검증단계에서 포함하지 않음

class BoxofficeMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxofficeMovie
        fields = '__all__'

class NaverMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = NaverMovie
        fields = '__all__'

class AgoBoxofficeMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgoBoxofficeMovie
        fields = '__all__'