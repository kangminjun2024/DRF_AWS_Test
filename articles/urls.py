from django.urls import path
from . import views

app_name = "articles"
urlpatterns = [
    # path("", views.article_list, name="article_list"),    # FBV 방식으로 사용할 때
    path("", views.ArticleListAPIView.as_view(), name="article_list"),  # CBV 방식으로 사용할때
    # path("<int:pk>/", views.article_detail, name="article_detail"),    #  FBV 방식, 근데 사실 api로 개발할 때는 name을 안쓴다. 심지어 DRF로 개발할 때는 app_name도 잘 안쓴다.
    path("<int:pk>/", views.ArticleDetailAPIView.as_view(), name="article_detail"), # CBV 방식으로 사용할때
    path("<int:article_pk>/comments/", 
        views.CommentListAPIView.as_view(), 
        name="comment_list"),
    path("comments/<int:comment_pk>/", 
        views.CommentDetailAPIView.as_view(), 
        name="comment_detail"),
    path("check-sql/", views.check_sql, name="check_sql"),
]
