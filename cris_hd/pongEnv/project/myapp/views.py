# this is where we put our request handler

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
   
def login(request):
  return render(request, 'login.html')

def home(request):
  return render(request, 'home.html')

def game(request):
  return render(request, 'game.html')

def edit(request):
  return render(request, 'edit.html')

def stats(request):
  return render(request, 'stats.html')

def friends(request):
  return render(request, 'friends.html')

def logout(request):
  language_code = request.GET.get('language', 'en')  # Default to English
  print(f"Detected language code: {language_code}")
  return render(request, 'logout.html')
