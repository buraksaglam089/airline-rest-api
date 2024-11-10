from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from .models import Aircraft
from .serializers import AircraftSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def aircraft_list(request):
    if request.method == 'GET':
        try:
            with transaction.atomic():
                aircraft = Aircraft.objects.select_related('operator_airline').all()
                serializer = AircraftSerializer(aircraft, many=True)
                return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'POST':
        try:
            with transaction.atomic():
                serializer = AircraftSerializer(data=request.data)
                if serializer.is_valid():
                    aircraft = serializer.save()
                    aircraft = Aircraft.objects.select_related('operator_airline').get(pk=aircraft.pk)
                    serializer = AircraftSerializer(aircraft)
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                    )
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            transaction.set_rollback(True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def aircraft_detail(request, pk):
    try:
        with transaction.atomic():
            aircraft = Aircraft.objects.select_related('operator_airline').get(pk=pk)
    except Aircraft.DoesNotExist:
        return Response(
            {'error': 'Aircraft not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if request.method == 'GET':
        try:
            with transaction.atomic():
                serializer = AircraftSerializer(aircraft)
                return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'PATCH':
        try:
            with transaction.atomic():
                serializer = AircraftSerializer(aircraft, data=request.data, partial=True)
                if serializer.is_valid():
                    aircraft = serializer.save()
                    aircraft = Aircraft.objects.select_related('operator_airline').get(pk=aircraft.pk)
                    serializer = AircraftSerializer(aircraft)
                    return Response(serializer.data)
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            transaction.set_rollback(True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'DELETE':
        try:
            with transaction.atomic():
                aircraft.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            transaction.set_rollback(True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )