from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import (
    GenericViewSet, ModelViewSet, ReadOnlyModelViewSet)

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsAuthorOrAnyReadOnly
from .serializers import (
    CommentAuthorSerializer, FollowSerializer, GroupSerializer, PostAuthorSerializer)
from posts.models import Follow, Group, Post


class BaseViewSet(ModelViewSet):
    permission_classes = (IsAuthorOrAnyReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(BaseViewSet):
    ordering_fields = ('created', )
    serializer_class = CommentAuthorSerializer

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.validated_data['post'] = post
        super().perform_create(serializer)

    def get_queryset(self):
        post = self.get_post()
        return post.comments


class PostViewSet(BaseViewSet):
    pagination_class = LimitOffsetPagination
    ordering_fields = ('bpub_date', )
    serializer_class = PostAuthorSerializer
    queryset = Post.objects.all()


class GroupViewSet(ReadOnlyModelViewSet):
    ordering_fields = ('title', )
    permission_classes = (AllowAny,)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class FollowViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    filter_backends = (DjangoFilterBackend, SearchFilter)
    ordering_fields = ('following__username', )
    search_fields = ('=following__username',)
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
