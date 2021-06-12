from django.http.response import JsonResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Review, Comment
from .serializers import ReviewSerializer, ReviewDetailSerializer,CommentSerializer
from django.http import HttpResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Create your views here.
@api_view(['GET'])
def review_list(request): 
    # 전체 리뷰정보
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def review_create(request):
    print(request)
    # 리뷰생성
    serializer =ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)

@api_view(['GET'])
def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        returnData = serializer.data
        returnData['username'] = review.user.username
        comments = review.comment_set.all()
        returnData['comments'] = []
        for comment in comments:
            returnData['comments'].append([comment.content, comment.user.username, comment.user_id])
        return JsonResponse(returnData)
        
@api_view(['PUT','DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_change(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'PUT':
        if review.user == request.user:
            serializer = ReviewDetailSerializer(review, request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            data = {
                'update': '수정 권한이 없습니다.',
            }
            return Response(data)
    elif request.method =='DELETE':
        if review.user == request.user:
            review.delete()
            data = {
                'delete': f'{review.title}이 삭제되었습니다.',
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        # else:
        #     data = {
        #         'delete': '삭제 권한이 없습니다.',
        #     }
        #     return Response(data)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_create(request, review_id):
    # /review/<int:review_id>/comments/
    # 댓글 생성시 review_id 필요
    review = get_object_or_404(Review, pk=review_id)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(review=review)
        return Response(serializer.data)

@api_view(['GET'])
def comment_list(request):
    # comments/
    # 모든 댓글 확인
    comments = get_list_or_404(Comment)
    # comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_id):
    # comments/<int:comments_id>/
    # 댓글 정보 반환
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        comment.delete()
        data = {
            'delete': f'리뷰의 {comment_id}번째 댓글을 삭제하였습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
        