from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/chatbot/', include("chatbot.urls")),
    path('api/pickups/', include('pickups.urls')),
    path('api/subscription/', include('subscription.urls')),
    path('api/location/', include('location.urls')),
    path('api/payment/', include('payment.urls')),
    path('api/assignment/', include('assignment.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

