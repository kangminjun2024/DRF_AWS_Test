from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema #1-14 강의
from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleDetailSerializer ,CommentSerializer


# FBV 방식은 주석처리   start
'''
#   전체조회
@api_view(["GET", "POST"])   # 반드시 함수형 view에는 api임을 알 수 있도록 데코레이터를 달아줘야한다.
def article_list(request):
    if request.method == "GET":
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True) # articles가 단일 객체라면 many가 false여도 됨
        return Response(serializer.data)
    
    # elif request.method == "POST":
    #     serializer = ArticleSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=201)    # status안해줘도 되는데 200번대가 성공인데 201번은 생성에 성공했다는 뜻이거든? 정확하게 집어주자고
    #     return Response(serializer.errors, status=400)
    
    elif request.method == "POST":
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):   #raise_exception 설정해주면 return Response(serializer.errors, status=400) 안해줘도된다
            serializer.save()
            # return Response(serializer.data, status=201)    # status안해줘도 되는데 200번대가 성공인데 201번은 생성에 성공했다는 뜻이거든? 정확하게 집어주자고
            return Response(serializer.data, status=status.HTTP_201_CREATED)    # 바로 위에 있는 코드랑 똑같다. 근데 이렇게 쓰는것을 권장하다.



# 하나 상세 조회 / 수정 / 삭제
@api_view(["GET", "DELETE", "PUT"])
def article_detail(request, pk):
    if request.method == "GET":
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article) # article상세조회하는거라 하나만 부를꺼라 many 필요없음
        return Response(serializer.data)

    elif request.method == "PUT":
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data, partial =True)   # partial를 설정해주면 제목만 수정해도되고, 내용만 수정해도된다. 즉, 부분수정 가능
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    elif request.method == "DELETE":
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
'''
# FBV 방식은 주석처리   end



# CBV 방식을 권장해용

class ArticleListAPIView(APIView):
    #1-10강의
    permission_classes = [IsAuthenticated]  #   여기서는 항상 Authenticated 된 것만 쓰겠다
    
    @extend_schema (#1-14강의   swagger에서 항목을 나눠주기 위한 데코레이션이다.
            tags=["Articles"],
            description="Article 목록 조회를 위한 API"
        )    
    def get(self, request):
        print(" 현재 사용자의 이름: ", request.user.username, "\n")
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True) # articles가 단일 객체라면 many가 false여도 됨
        return Response(serializer.data)
    
    @extend_schema (#1-14강의   swagger에서 항목을 나눠주기 위한 데코레이션이다.
            tags=["Articles"],
            description="Article 생성를 위한 API",
            request=ArticleSerializer,
        ) 
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):   #raise_exception 설정해주면 return Response(serializer.errors, status=400) 안해줘도된다
            serializer.save()
            # return Response(serializer.data, status=201)    # status안해줘도 되는데 200번대가 성공인데 201번은 생성에 성공했다는 뜻이거든? 정확하게 집어주자고
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class ArticleDetailAPIView(APIView):
    #1-10강의
    permission_classes = [IsAuthenticated]  #   여기서는 항상 Authenticated 된 것만 쓰겠다
    
    def get_object(self, pk):   #1-7강의, 그냥 코드 줄여주기 위한 함수임
        return get_object_or_404(Article, pk=pk)
    
    def get(self, request, pk):
        article = self.get_object(pk=pk)
        serializer = ArticleDetailSerializer(article) # article상세조회하는거라 하나만 부를꺼라 many 필요없음
        return Response(serializer.data)
    
    def put(self, request, pk):
        article = self.get_object(pk=pk)
        serializer = ArticleDetailSerializer(article, data=request.data, partial =True)   # partial를 설정해주면 제목만 수정해도되고, 내용만 수정해도된다. 즉, 부분수정 가능
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
    def delete(self, request, pk):
        article = self.get_object(pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListAPIView(APIView):
    #1-10강의
    permission_classes = [IsAuthenticated]  #   여기서는 항상 Authenticated 된 것만 쓰겠다

    def get(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)    #return Response({}, status=status.HTTP_201_CREATED) 이렇게해도된다
        

class CommentDetailAPIView(APIView):    #1-8 강의
    #1-10강의
    permission_classes = [IsAuthenticated]  #   여기서는 항상 Authenticated 된 것만 쓰겠다

    def get_object(self, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk)
    
    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#   ORM 최적화를 위해 쿼리 줄이기
@api_view(["GET"])
def check_sql(request):
    from django.db import connection    #   쿼리를 보기 위해 사용
    
#    comments = Comment.objects.all().select_related("article") # select_related() 정참조   1:1, 1:다일 때 join할 때,
#    for comment in comments:
#        print(comment.article.title)
#   print("\n\n## connection.queries ##\n ", connection.queries, "\n")
    
    articles = Article.objects.all().prefetch_related("comments")   # prefetch_related() 역참조 다:다일 때, 쿼리를 두번 날리면서 사용될때 근데 정참조일 때도 쓸수있다.
    for article in articles:
        comments = article.comments.all()
        for comment in comments:
            print(comment.content)

    print("\n\n## connection.queries ##\n ", connection.queries, "\n")  # 쿼리를 한번 보자

#   썩은 쿼리 보여주기
#    articles = Article.objects.all()
#    for article in articles:
#        comments = article.comments.all()
#        for comment in comments:
#            print(comment.content)

#    print("\n\n## connection.queries ##\n ", connection.queries, "\n") 
    
    
    return Response()