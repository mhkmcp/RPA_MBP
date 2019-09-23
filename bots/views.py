# Create your views here.
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def worker_bot(request):
    if request.method == 'GET':
        print("executing worker bot")

    return Response({"status": True}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def nid_bot(request):
    if request.method == 'GET':
        print("executing nid bot")

    return Response({"status": True}, status=status.HTTP_200_OK)
