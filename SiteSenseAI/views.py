from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from site_sense_lib.lib.site_sense import SiteSense


# Create your views here.
def home(request) -> HttpResponse:
    return render(request, "SiteSenseAI/index.html", {})


def emily_ai(request) -> HttpResponse:
    chat_memory = request.session.get('conversation_memory', [])
    site_sense: SiteSense = SiteSense(model="gpt-3.5-turbo", temp=0.7, memory_data=chat_memory)

    if request.method == "POST":
        question = request.POST.get("question")
        response = site_sense.get_response(question)
        request.session['conversation_memory'] = site_sense.update_memory(question, response)

        # context: dict = {
        #     "question": question,
        #     "response": response.replace("Emily:", ""),
        #     "chat_history": chat_memory,
        # }

        context: dict = {
            "response": response.replace("Emily:", ""),
        }

        return JsonResponse(context)
    return render(request, "SiteSenseAI/emily_ai.html", {})
