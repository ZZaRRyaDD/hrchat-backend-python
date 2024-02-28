from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


urlpatterns = [
    path(
        'student/',
        views.StudentAuthAPIView.as_view(),
        name='access_token_student',
    ),
    path(
        'trainer/',
        views.TrainerAuthAPIView.as_view(),
        name='access_token_trainer',
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='refresh_token_generate',
    ),
]
