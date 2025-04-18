from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PhoneRange
import re


@api_view(['GET'])
def check_phone(request):
    phone = request.GET.get('phone', '').strip()

    # Валидация номера
    if not re.match(r'^7\d{10}$', phone):
        return Response(
            {'error': 'Неверный формат номера. Номер должен быть в формате 7XXXXXXXXXX (11 цифр)'},
            status=status.HTTP_400_BAD_REQUEST
        )

    abc = phone[1:4]
    number = int(phone[4:])

    try:
        # Ищем диапазон, в который попадает номер
        range = PhoneRange.objects.filter(
            abc=abc,
            start__lte=number,
            end__gte=number
        ).first()

        if range:
            return Response({
                'phone': phone,
                'operator': range.operator,
                'region': range.region,
                'inn': range.inn
            })
        else:
            return Response(
                {'error': 'Номер не найден в базе данных'},
                status=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )