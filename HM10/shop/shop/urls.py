from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from api.urls import urlpatterns as api_urlpatterns

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urlpatterns)),
    path('', include('users.urls')),
    path('', include('feedback.urls')),
    path('', include('products.urls')),
    path('', include('orders.urls')),
    path('', include('favorite.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
]

if settings.DEBUG:  # pragma: no cover
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
