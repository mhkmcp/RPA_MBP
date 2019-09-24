# Create your views here.
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from bank_asia_scripts.Parallel_process import *
from bank_asia_scripts.Creating_info import *
from bots.tasks import add, mul


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def worker_bot(request):
    if request.method == 'GET':
        add.delay()

    return Response({"status": True}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def nid_bot(request):
    if request.method == 'GET':
        print("executing nid bot")
        mul.delay()


    return Response({"status": True}, status=status.HTTP_200_OK)
