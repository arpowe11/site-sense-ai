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
        prompt = site_sense.create_response(question=question)
        response = site_sense.stream_response(prompt)
        # response_message = f"\n\nYou said: {response}"

        return JsonResponse({'message': response})
