from django.urls import path

from . import views

urlpatterns = [
    path('rooms/', views.RoomCreateAPIView.as_view(), name='room-create'),
    path(
        'results/<uuid:room_uuid>/',
        views.ResultsTrainingAPIView.as_view(),
        name='get-results',
    ),
]
