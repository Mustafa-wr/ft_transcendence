from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .models import RegistrationForm
from .models import Match
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext


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

def edit(request):
  return render(request, 'edit.html')

def stats(request):
	matches = Match.objects.all().select_related('winner_user', 'loser_user')
	return render(request, 'stats.html', {'matches': matches})

def friends(request):
  return render(request, 'friends.html')

def logout(request):
  return render(request, 'logout.html')

# def switch_language(request, language):
#     activate(language)
#     old_path = request.META.get('HTTP_REFERER', None)
#     print(f"ultimo url-> {old_path}")
#     if old_path:
#         path_parts = old_path.split('/')
#         print(f"todos os paths-> {path_parts}")
#         last_part = path_parts[-1] or path_parts[-2]
#         if last_part:
#             print(f"ultima parte da url-> {last_part}")
#             return redirect(last_part)
#     return redirect('home')
