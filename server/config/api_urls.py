from django.urls import include, path


urlpatterns = [
    path('auth/', include('apps.users.urls')),
    path('trainings/', include('apps.trainings.urls')),
]
