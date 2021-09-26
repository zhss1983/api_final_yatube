from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from posts.models import Comment, Group, Post, Follow, User


class PostSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)

class GroupSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group

class FollowSerializer(ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True)
    following = SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Follow

    def validate_following(self, value):
        user = self.context['request'].user
        not_user = value != user
        not_exist = not user.follower.filter(following=value).exists()
        if value != user and not user.follower.filter(following=value).exists():
            return value
        raise ValidationError(
                'Отсутствует обязательное поле в теле запроса или оно не '
                'соответствует требованиям'
              )
