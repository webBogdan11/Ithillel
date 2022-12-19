from django.urls import path, include

from api.products.urls import urlpatterns as products_urlpatterns
from api.feedback.urls import urlpatterns as feedbacks_urlpatterns
from api.user_api.urls import urlpatterns as user_urlpatterns

urlpatterns = [
    path('', include(products_urlpatterns)),
    path('', include(feedbacks_urlpatterns)),
    path('', include(user_urlpatterns)),
    path('api-auth/', include('rest_framework.urls'))
]
