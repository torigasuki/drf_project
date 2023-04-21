from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.query_utils import Q
from rest_framework import status, permissions
from articles.models import Article,Comment
from articles.serializers import ArticleSerializer,ArticleListSerializer,ArticleCreateSerializer,CommentSerializer,CommentCreateSerializer

class ArticleView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        selializer = ArticleListSerializer(articles, many=True)
        return Response(selializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response("로그인이 필요합니다.", status=status.HTTP_401_UNAUTHORIZED) 
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        q=Q()
        for user in request.user.followings.all():
            q.add(Q(user=user), q.OR)
        feeds = Article.objects.filter(q)
        serializer = ArticleListSerializer(feeds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ArticleDetailView(APIView):
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            serializer = ArticleCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("ㅗㅗㅓㄴ한이 업어!",status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("ㅗㅗㅓㄴ한이 업어!",status=status.HTTP_403_FORBIDDEN)


class CommentView(APIView):
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        comment = article.comment_set.all()
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request ,article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def put(self, request, article_id,comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("ㅗㅗㅓㄴ한이 업어!",status=status.HTTP_403_FORBIDDEN)


    def delete(self, request, article_id,comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("ㅗㅗㅓㄴ한이 업어!",status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView):
    def get(self, request,article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response("좋아요 취소", status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response("좋아요", status=status.HTTP_200_OK)

    def post(self, request,article_id):
        pass