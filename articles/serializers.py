# 마치 model form처럼 동작한다

from rest_framework import serializers
from .models import Article, Comment

# 댓글
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("article", )  # article은 읽기 전용 필드라고 알려줘야지 안그러면 post로 댓글 생성할 때 article이라는 외래키 속성도 참조하느라 댓글이 안 써진다.
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)   # CommentSerializer클래스의 결과를 ret에 넣었다
        ret.pop("article")  # article 빼버리고
        return ret
        
# 게시글
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        
#   ArticleSerializer를 상속받은 클래스 디테일로 볼때만 댓글 나오게
class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
        # comments.count이거 ORM이다. Comment.object.all().count()라는 얘기다.
