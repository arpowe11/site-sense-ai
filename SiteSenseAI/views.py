from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from site_sense_lib.lib.site_sense import SiteSense


def index(request) -> HttpResponse:
    return render(request, 'SiteSenseAI/index.html', {})


def chatbot(request) -> HttpResponse:
    return render(request, 'SiteSenseAI/chatbot.html', {})


def chatbot_response(request):
    memory_data = request.session.get('conversation_memory', None)
    site_sense: SiteSense = SiteSense(model="gpt-3.5-turbo", temp=0.7, memory_data=memory_data)

    if request.method == 'POST':
        question = request.POST.get('question')

        response = site_sense.chat_bot(question)
        result = response
        request.session['conversation_memory'] = site_sense.get_memory_data()


        return render(request, 'SiteSenseAI/chatbot.html', {'response': result})
    return render(request, 'SiteSenseAI/chatbot.html', {})
