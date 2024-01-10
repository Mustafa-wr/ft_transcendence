from django.shortcuts import render #http://157.245.40.149:30655
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .models import RegistrationForm
from .models import Match
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from django.shortcuts import render, redirect


def stats_view(request):
    users = user_data.objects.all()  # Fetch all User objects
    return render(request, 'stats.html', {'users': users})


def base(request):
	return render(request, 'base.html')

def login(request):
    # Check if the user is already authenticated
    if request.method == 'GET':
        print(f"am heeree{request.user.is_authenticated}")
    if request.user.is_authenticated:
	    return redirect('/home')
    user_info = request.session.get('user_info')
    print(f"am heeree{user_info}")
    if user_info:
        # If already authenticated, redirect to home or dashboard
        return redirect('home')
    return render(request, 'login.html')

    # Your login logic goes here...
    # If the login is successful and the user is authenticated:
    # Set the user_info in the session
    # request.session['user_info'] = user_info  # Replace with your authenticated user info

    # Then redirect to home or dashboard

def authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        user_info = request.session.get('user_info')
        if user_info:
            # User is authenticated, allow access to the view
            return view_func(request, *args, **kwargs)
        else:
            print("not authenticated")
            # User is not authenticated, redirect to the login page
            return redirect('login')
    return wrapper


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

@authenticated_user
def index(request):
    return render(request, 'index.html')
@authenticated_user
def game(request):
    return render(request, 'game.html')

def authorize(request):
    client_id = "client_id=u-s4t2ud-8156fc58fc2005216ad58258e48c1a311ceb0c4b4bd45451aba59272720501f4"
    redirect_uri = f"http://{request.get_host()}/callback"

    authorization_url = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"

    return redirect('/home/')

# def login(request):
#   return render(request, 'login.html')
  
@authenticated_user
def home(request):
  return render(request, 'home.html')

def edit(request):
  return render(request, 'edit.html')

def stats(request):
	matches = Match.objects.all().select_related('winner_user', 'loser_user')
	return render(request, 'stats.html', {'matches': matches})

def friends(request):
  return render(request, 'friends.html')

@authenticated_user
def logout(request):
    # Remove the user_info from the session
    if 'user_info' in request.session:
        del request.session['user_info']
    
    # Redirect to a page indicating successful logout or any other desired page
    return redirect('home')  # Replace 'home' with the URL name of your desired page


# def switch_language(request, language):
#     activate(language)
#     old_path = request.META.get('HTTP_REFERER', None)
#     last_part = None
#     # try:
#     if old_path:
# 	# Split the URL by '/'
#         path_parts = old_path.split('/')
# 	# Take the last part of the URL
#         last_part = path_parts[-1]
# 	#   print(path_parts)
#     print(f"am heeree{last_part}")
# 	# Now, last_part contains the last part of the URL
#     print(f"ultima parte-> {last_part}")
#     if last_part:
# 	    return redirect(last_part)
#     return redirect('home')




    # except Exception as e:
    #     return HttpResponseServerError(f"An error occurred: {e}")

# from django.http import Http404

# def switch_language(request, language):
#     try:
#         activate(language)
#         old_path = request.META.get('HTTP_REFERER', None)
#         last_part = None
        
#         if old_path:
#             path_parts = old_path.split('/')
#             last_part = path_parts[-1]
        
#         print(f"am heeree{last_part}")
#         print(f"ultima parte-> {last_part}")
        
#         if last_part:
#             return redirect(last_part)
#         return redirect('home')
    
#     except Exception as e:
#         # Handle the exception here
#         print(f"An error occurred: {str(e)}")
#         raise Http404("Page not found")
