from django.shortcuts import render
import requests

def home(request):
    context = {}
    if request.method == 'GET' and 'phone' in request.GET:
        phone = request.GET['phone'].strip()
        if phone:
            context['phone'] = phone
            try:
                response = requests.get(
                    f'http://{request.get_host()}/api/check_phone/',
                    params={'phone': phone}
                )
                if response.status_code == 200:
                    data = response.json()
                    context.update(data)
                else:
                    context['error'] = response.json().get('error', 'Произошла ошибка')
            except Exception as e:
                context['error'] = str(e)
    return render(request, 'phone_checker/index.html', context)