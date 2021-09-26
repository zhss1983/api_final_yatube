from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import CommentViewSet, GroupViewSet, PostViewSet, FollowViewSet

api_router_v1 = DefaultRouter()
api_router_v1.register('posts', PostViewSet, basename='posts')
api_router_v1.register('groups', GroupViewSet, basename='groups')
api_router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
api_router_v1.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    #path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(api_router_v1.urls)),
]