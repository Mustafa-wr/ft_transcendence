from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .models import RegistrationForm

# Create your views here.

def base(request):
	return render(request, 'base.html')

# def sign_up(request):
# 	if request.method == 'POST':
# 		form = RegistrationForm(request.POST)
# 		if form.is_valid():
# 			user = form.save()
# 			login(request, user)
# 			return redirect('home')
# 	else:
# 		form = RegistrationForm()

# 	return render(request, 'registration/sign-up.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def game(request):
    return render(request, 'game.html')

def authorize(request):
    client_id = "client_id=u-s4t2ud-8156fc58fc2005216ad58258e48c1a311ceb0c4b4bd45451aba59272720501f4"
    redirect_uri = "http://127.0.0.1:8000/callback"
    
    authorization_url = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    
    return redirect(authorization_url)


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

