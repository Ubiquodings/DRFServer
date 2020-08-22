from django.shortcuts import render

# test api
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def test_api(request):
    return Response({"message": "ok."}, status=status.HTTP_200_OK)
