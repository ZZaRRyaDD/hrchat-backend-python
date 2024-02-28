from rest_framework import generics

from ..serializers import StudentAuthSerializer


class StudentAuthAPIView(generics.CreateAPIView):
    serializer_class = StudentAuthSerializer
