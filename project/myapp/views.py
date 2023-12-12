from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.

def index(request):
    return render(request, 'index.html')

def game(request):
    return render(request, 'game.html')

def authorize(request):
    client_id = "client_id=u-s4t2ud-8156fc58fc2005216ad58258e48c1a311ceb0c4b4bd45451aba59272720501f4"
    redirect_uri = "http://127.0.0.1:8000/callback"
    
    authorization_url = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    
    return redirect(authorization_url)
