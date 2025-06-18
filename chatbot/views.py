# chatbot/views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
#from .ai_module import get_chatbot_response  # your function using LangChain or similar
from .agent import ask_question
import json

@csrf_exempt
def chatbot_ask(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question = data.get("question", "")
        response = ask_question(question)
        return JsonResponse({"answer": response})

# def chatbot_ui(request):
#     return render(request, ".html")
