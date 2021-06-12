from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework import response
from community.models import Review, Comment
from movies.models import TmdbMovie
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserListSerializer
from django.core import serializers
from community.serializers import ReviewSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Create your views here.
# 에러코드 추가해야함
@api_view(['POST'])
def signup(request):
    # client에서 넘어오는 데이터
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')

    # 비번확인
    if password != password_confirmation:
        return Response({"error": '비밀번호를 확인해주세요!'})

    # JSON으로 보내야하니까?
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
        return Response(serializer.data)

@api_view(['GET'])
def profile(request, user_pk):
    # 좋아요를 누른 유저의 pk값이 1번이라면
    # 1번 유저가 누른 영화의 목록을 받아오는거지
    person = get_object_or_404(get_user_model(), pk=user_pk)
    # 모든 Tmdbmovie의 라이크유저를 받아옴
    likemovies = serializers.serialize('json', person.like_movies.all())
    review = serializers.serialize('json', person.review_set.all())
    comment = serializers.serialize('json', person.comment_set.all())
    context = {
        'review': review,
        'comment': comment,
        'likemovies': likemovies,
        'username': person.username,
    }
    context['count_followers'] = person.followers.count()
    context['count_followings'] = person.followings.count()
    return JsonResponse(context)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    person = get_object_or_404(get_user_model(), pk=user_pk)
    user = request.user
    context = {}
    if person != user:
        if person.followers.filter(pk=user.pk).exists():
            person.followers.remove(user)
            follow = False
        else:
            person.followers.add(user)
            follow = True
        context = {
            'follow' : follow,
            'count_followers' : person.followers.count(),
            'count_followings' : person.followings.count(),
        }
    return JsonResponse(context)
