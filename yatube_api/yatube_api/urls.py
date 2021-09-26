from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]

# Подключение автоматической документации.

schema_view = get_schema_view(
   openapi.Info(
      title="Документация к API проекта Yatube",
      default_version='v1',
      description="",
      # terms_of_service="URL страницы с пользовательским соглашением",
      contact=openapi.Contact(email="zhss1983@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^api/swagger(?P<format>\.json|\.yaml)$',
       schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui'),
   url(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
       name='schema-redoc'),
]
