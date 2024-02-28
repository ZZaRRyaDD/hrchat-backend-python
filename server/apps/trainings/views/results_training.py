from tempfile import NamedTemporaryFile

from rest_framework import views
from django.core.files.base import ContentFile
from django.http import HttpResponse

from ..models import Room
from ..serializers import ResultsTrainingParamsSerializer
from ..permissions import TrainerPermission
from ..utils import get_results_training


class ResultsTrainingAPIView(views.APIView):
    permission_classes = (TrainerPermission, )

    def get(self, request, *args, **kwargs):
        serializer = ResultsTrainingParamsSerializer(
            data=self.kwargs,
        )
        serializer.is_valid(raise_exception=True)
        with NamedTemporaryFile() as file_obj:
            room = (
                Room.objects.prefetch_related(
                    'rounds', 'rounds__messages', 'students',
                ).get(
                    uuid=serializer.data['room_uuid'],
                )
            )
            get_results_training(
                room,
                file_obj.name,
            )
            file_to_send = ContentFile(file_obj.read())
            filename = f'results-{room.uuid}'
            response = HttpResponse(file_to_send, 'application/x-gzip')
            response['Content-Length'] = file_to_send.size
            response['Content-Disposition'] = (
                f'attachment; filename="{filename}.xlsx"'
            )
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            return response
