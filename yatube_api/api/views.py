from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer, FollowSerializer
from posts.models import Group, Post, Follow, User


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthorOrReadOnly, )
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer
#    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly, )
    serializer_class = CommentSerializer
    pagination_class = None

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = self.get_post()
        return post.comments


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('following__username',)
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)


