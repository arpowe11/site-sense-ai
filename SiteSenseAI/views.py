from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from site_sense_lib.lib.site_sense import SiteSense


def index(request) -> HttpResponse:
    return render(request, 'SiteSenseAI/index.html', {})


def chatbot(request) -> HttpResponse:
    return render(request, 'SiteSenseAI/chatbot.html', {})


def chatbot_response(request):
    if request.method == 'POST':
        question = request.POST.get('message')

        # Here you would implement your chatbot logic
        site_sense: SiteSense = SiteSense(model="gpt-3.5-turbo", temp=0.4)  # NOQA
        response = site_sense.chat_bot(question)

        return JsonResponse({'message': response["response"]})
