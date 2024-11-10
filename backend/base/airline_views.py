from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from .models import Airline
from .serializers import AirlineSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def airline_list(request):
    if request.method == 'GET':
        try:
            with transaction.atomic():
                airlines = Airline.objects.prefetch_related('aircraft_set').all()
                serializer = AirlineSerializer(airlines, many=True)
                return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'POST':
        try:
            with transaction.atomic():
                serializer = AirlineSerializer(data=request.data)
                if serializer.is_valid():
                    airline = serializer.save()
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
def airline_detail(request, pk):
    try:
        with transaction.atomic():
            airline = Airline.objects.prefetch_related('aircraft_set').get(pk=pk)
    except Airline.DoesNotExist:
        return Response(
            {'error': 'Airline not found'},
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
                serializer = AirlineSerializer(airline)
                return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'PATCH':
        try:
            with transaction.atomic():
                serializer = AirlineSerializer(airline, data=request.data, partial=True)
                if serializer.is_valid():
                    airline = serializer.save()
                    airline = Airline.objects.prefetch_related('aircraft_set').get(pk=airline.pk)
                    serializer = AirlineSerializer(airline)
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
                airline.delete()
                return Response(
                    status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            transaction.set_rollback(True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )