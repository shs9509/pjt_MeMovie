from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.relations import ManyRelatedField
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import render
from django.utils import timezone
from django.core import serializers
from .models import TmdbMovie, BoxofficeMovie, MovieComment, NaverMovie, AgoBoxofficeMovie
from datetime import datetime, timedelta
from .serializer import MovieCommentSerializer, MovieSerializer, BoxofficeMovieSerializer, NaverMovieSerializer ,AgoBoxofficeMovieSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.db.models import Max
import json, requests
from django.db.models import Q
import os
import sys
import requests
import pandas as pd

# Create your views here.

@api_view(['GET'])
def index(request):
    # 0. Naver + tmdb
    movies = NaverMovie.objects.all()
    if not movies:
        today = datetime.now()
        yearsago_day = today + timedelta(days=-(365*3))
        yearsago_day= str(yearsago_day)[0:4].replace("-","")
        client_id = "secret_ID"
        client_secret = "secret"
        header_parms ={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
        url = f"https://openapi.naver.com/v1/search/movie.json?query='<b>'&display=50"
        res=requests.get(url,headers=header_parms)
        print(res)
        datas =res.json()
        cnt = 0
        for data in datas['items']:
            cnt += 1
            if int(yearsago_day)>=int(data['pubDate']):
                movie = NaverMovie(
                    pk = cnt,
                    movie_title=data['title'].strip('</b>').replace('<b>','').replace('</b>',''),
                    original_title=data['subtitle'].strip('</b>').replace('<b>','').replace('</b>',''),
                    overview=data['link'],
                    poster_path=data['image'],
                    genre=0,
                    release_date=data['pubDate'],
                    vote_average=float(data['userRating']),
                )
                movie.save()
            else:
                continue
        movies = NaverMovie.objects.all()
    # print(movies, '?????? naver')
    serializer = NaverMovieSerializer(movies, many=True)
    naver = serializer.data

    # 1. Tmdb
    movies = TmdbMovie.objects.all()
    if not movies:
        cnt = 0
        for page in range(1, 6):
            movies = requests.get(f'https://api.themoviedb.org/3/movie/top_rated?api_key=3bbc026192666f6007f1cdda0c8da2ec&language=ko-KR&page={page}')
            movies = movies.json()['results']
            for movie in movies:
                cnt += 1
                new_movie = TmdbMovie(
                    pk = cnt,
                    movie_title=movie.get('title'),
                    original_title=movie.get('original_title'),
                    overview=movie.get('overview'),
                    poster_path=movie.get('poster_path'),
                    genre=str(movie.get('genre_ids')[0]),
                    release_date=movie.get('release_date'),
                    vote_average=movie.get('vote_average'),
                )
                new_movie.save()
        movies = TmdbMovie.objects.all()
        # ???????????? tmdb??? naver??? ??????
    # print(movies, '?????? tmdb')
    serializer = MovieSerializer(movies, many=True)
    tmdb = serializer.data

    # 2. Boxoffice
    movies = BoxofficeMovie.objects.all()
    today = datetime.now()
    start_day = today + timedelta(days =- 10)
    key='secret_key'
    client_id = "secret_id"
    client_secret = "secret_secret"
    header_parms ={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
 
    # https://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key=59071dc564dedb5e07afe9dcb11dbe72&targetDt=20120101
    if not movies:
        # start_day = start_day + timedelta(days=1)
        # print(start_day)
        day= str(start_day)[0:10].replace("-","")
        # print(day)
        box_office = requests.get(f'https://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={key}&targetDt={day}')
        box_office = box_office.json()['boxOfficeResult']
        cnt = 0
        now_show_range = box_office.get('showRange')[:8]
        for movie in box_office['dailyBoxOfficeList']:
            box_movie=movie.get('movieNm')
            url = f"https://openapi.naver.com/v1/search/movie.json?query={box_movie}"
            res=requests.get(url,headers=header_parms)
            data =res.json()  
            cnt +=1
            new_movie = BoxofficeMovie(
                    pk = cnt,
                    movie_title=movie.get('movieNm'),
                    poster_path= data['items'][0]['image'],
                    show_range =now_show_range,
                    rank=movie.get('rank'),
                    audi=movie.get('audiAcc'),
                    sales=movie.get('salesAcc'),
                )
            new_movie.save()
    movies = BoxofficeMovie.objects.all()
    # print(movies, '?????? boxoffice')
    serializer = BoxofficeMovieSerializer(movies, many=True)
    boxoffice = serializer.data
    # print('boxoffice@@@@@@@@@@@@@@@@@',boxoffice)
    # print(type(boxoffice))
    context={
        'naver': naver,
        'tmdb': tmdb,
        'boxoffice': boxoffice,
    }
    # print('naver@@@@@@@@@@@@',context['naver'])
    # print()
    # print('tmdb@@@@@@@@@@@@',context['tmdb'])
    # print()
    # print('boxoffice@@@@@@@@@@@@',context['boxoffice'])
    # print()
    return JsonResponse(context)

# 1?????? 3?????? 5?????? ??????????????? ??????????????????
@api_view(['GET'])
def recommend(request):
    # ?????????
    client_id = "secret_id"
    client_secret = "secret_secret"
    header_parms ={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}

    # ?????? ?????????
    AgoBoxofficeMovie.objects.all().delete()
    today = datetime.now()
    cnt = 0
    for i in [1,3,5]:
        years_ago = today + timedelta(days=-(365*i))
        years_ago= str(years_ago)[0:10].replace("-","")
        key='secret_key'
        # https://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key=59071dc564dedb5e07afe9dcb11dbe72&targetDt=20120101
        box_office = requests.get(f'https://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={key}&targetDt={years_ago}')
        box_office = box_office.json()['boxOfficeResult']
        now_show_range = box_office.get('showRange')[:8]
 

        for movie in box_office['dailyBoxOfficeList']:
            box_movie=movie.get('movieNm')
            url = f"https://openapi.naver.com/v1/search/movie.json?query={box_movie}"
            res=requests.get(url,headers=header_parms)
            data =res.json()  
            cnt +=1
            new_movie = AgoBoxofficeMovie(
                    pk = cnt,
                    movie_title=movie.get('movieNm'),
                    poster_path= data['items'][0]['image'],
                    show_range =now_show_range,
                    rank=movie.get('rank'),
                    audi=movie.get('audiAcc'),
                    sales=movie.get('salesAcc'),
                )
            new_movie.save()
    movies = AgoBoxofficeMovie.objects.all()
    BoxOffice = serializers.serialize('json', movies)
    return HttpResponse(BoxOffice, content_type='application/json')


@api_view(['GET'])
def movie_detail(request, movie_id):
    movie = get_object_or_404(TmdbMovie, pk= movie_id)
    comments = movie.moviecomment_set.all()
    Comments = MovieCommentSerializer(comments,many=True)
    count = movie.like_users.all().count()
    if request.user in movie.like_users.all():
        like=True
    else:
        like=False
    serializer = MovieSerializer(movie)
    context = {
        'movie':serializer.data,
        'comments':Comments.data,
        'like':like,
    }
    return Response(context)

@api_view(['GET'])
def naver_movie_detail(request, movie_id):
    movie = get_object_or_404(NaverMovie, pk= movie_id)
    serializer = NaverMovieSerializer(movie)
    context = {
        'movie':serializer.data,
    }
    return Response(context)

@api_view(['GET'])
def boxoffice_movie_detail(request, movie_id):
    movie = get_object_or_404(BoxofficeMovie, pk= movie_id)
    serializer = BoxofficeMovieSerializer(movie)
    context = {
        'movie':serializer.data,
    }
    return Response(context)

# ????????? ?????? ??????
@api_view(['POST'])
def comment_create(request, movie_id):
    tmdbmovie = get_object_or_404(TmdbMovie, pk=movie_id)
    serializer = MovieCommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=tmdbmovie)
        return Response(serializer.data)

@api_view(['GET'])
def comment_list(request):
    # ?????? ?????? ??????
    comments = get_list_or_404(MovieComment)
    serializer = MovieCommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, comment_id):
    # ?????? ?????? ??????
    comment = get_object_or_404(MovieComment, pk=comment_id)
    if request.method == 'GET':
        serializer = MovieCommentSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MovieCommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        comment.delete()
        data = {
            'delete': f'{comment_id}?????? ????????? ?????????????????????.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)



## ?????????
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def like(request,movie_id):
    if request.method == 'GET':
        movie = get_object_or_404(TmdbMovie, pk=movie_id)
        if request.user in movie.like_users.all():
            return Response(True, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(False, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'POST':
        movie = get_object_or_404(TmdbMovie, pk=movie_id)
        if request.user in movie.like_users.all():
            movie.like_users.remove(request.user)
            like=False
        else:
            movie.like_users.add(request.user)
            like =True
        context ={
            'like':like
        }    
        return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def user_recommend(request,user_id):
    if MovieComment.objects.filter(user=user_id):
        comments = MovieComment.objects.all().order_by('-rate').filter(user=user_id)
        best_movie_comment = comments[0]
        best_movie = TmdbMovie.objects.get(pk=best_movie_comment.movie.id)
        recommend_movie  = TmdbMovie.objects.all().filter(genre=best_movie.genre).filter(~Q(pk=best_movie.id))
        if not recommend_movie:
            data={
            'alert': '????????????????????? ????????? ???????????? ????????????.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        else:
            recommend_movie = MovieSerializer(recommend_movie, many=True)
            context = {
                'movies': recommend_movie.data,
            }
            return JsonResponse(context)
    else:
        data={
            'alert': '????????? ?????? ????????? ????????? ????????????????????????.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

        # ???????????? ????????? ????????? 1?????? ????????? ?????????????????? ????????? ????????? ??????????????????????? ?????????..
