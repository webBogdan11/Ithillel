from rest_framework.routers import DefaultRouter

from api.user_api.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user_api')
urlpatterns = router.urls
