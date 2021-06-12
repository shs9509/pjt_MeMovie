from django.db.models.fields import IntegerField
from rest_framework import serializers
from .models import Review, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',) # 검증단계에서 포함하지 않음

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('user','title','movie_title','content','created_at','updated_at','id')

class ReviewDetailSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(
        source='comment_set.count',
        read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie',)
