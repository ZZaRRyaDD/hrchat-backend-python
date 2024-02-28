from rest_framework_simplejwt.views import TokenObtainPairView

from ..serializers import TrainerAuthSerializer


class TrainerAuthAPIView(TokenObtainPairView):
    serializer_class = TrainerAuthSerializer
