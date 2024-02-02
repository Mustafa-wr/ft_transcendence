from django.shortcuts import render #http://157.245.40.149:30655
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import user_profile, match_record, user_friends, Create_match_record
from .models import user_profile, match_record, Game, Match_maker
from . import forms
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import UserProfileForm
from django.contrib import messages
from django.utils import translation
from django.views.i18n import set_language
from django.contrib.auth import logout

import json

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

@authenticated_user
def edit(request):
	profile = user_profile.objects.filter(login=request.session['user_info'].get('login')).first()
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			profile = form.save(commit=False)
			if profile.image:  # Check if an image is uploaded
				profile.image_link = profile.image.url
			profile.save()
			return redirect('edit')
	else:
		form = UserProfileForm(instance=profile)

	return render(request, 'base.html', {'form': form, 'user': profile})

@authenticated_user
def stats(request):
    current_user_login = request.session['user_info'].get('login')
    current_user = get_object_or_404(user_profile, login=current_user_login)

    matches = match_record.objects.filter(Q(match_winner=current_user) | Q(match_loser=current_user))
    match_count = matches.count()

    return render(request, 'base.html', {'matches': matches, 'match_count': match_count})

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

@authenticated_user
def index(request):
    return render(request, 'index.html')

@authenticated_user
def game(request):
    return render(request, 'game.html')

# @authenticated_user
# def pong(request):
# 	user = user_profile.objects.filter(login=request.session['user_info'].get('login')).first()
# 	return render(request, 'pong.html', {'user': user})

@authenticated_user
def pong(request):
		if (Match_maker.objects.all().count() == 0):
				Match_maker.objects.create()
		if request.method == 'GET':
			match_maker = Match_maker.objects.first()
			match_maker.players.remove(user_profile.objects.filter(login=request.session['user_info'].get('login')).first())
			match_maker.players.add(user_profile.objects.filter(login=request.session['user_info'].get('login')).first())
			if (match_maker.players.count() > 1):
				game_instance = Game()
				game_instance.player_1 = match_maker.players.all().first()
				match_maker.players.remove(game_instance.player_1)
				game_instance.player_2 = match_maker.players.all().first()
				match_maker.players.remove(game_instance.player_2)
				template = loader.get_template('pong.html')
				context = {
					'game': game_instance,
				}
				return HttpResponse(template.render(context, request))
			else:
				return redirect('home')
		else:
			if request.method == 'POST':
				data = json.loads(request.body)
				match_record_instance = match_record()
				match_record_instance.match_winner = user_profile.objects.filter(login=data['match_winner']).first()
				match_record_instance.match_loser = user_profile.objects.filter(login=data['match_loser']).first()
				match_record_instance.winner_score = data['winner_score']
				match_record_instance.loser_score = data['loser_score']
				match_record_instance.save()
				# return JsonResponse({'status': 'success'})
			return redirect('home')			
		
			
			
		
    

def authorize(request):
    client_id = "client_id=u-s4t2ud-53a3167e09d6ecdd47402154ef121f68ea10b4ec95f2cb099cf3d92e56a0c822"
    redirect_uri = f"http://{request.get_host()}/callback"

    authorization_url = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"

    return redirect('/home/')

@authenticated_user
def home(request):
  user = user_profile.objects.filter(login=request.session['user_info'].get('login')).first()
  return render(request, 'base.html', {'user':user})

@authenticated_user
def friends(request):
	user = user_profile.objects.filter(login=request.session['user_info'].get('login')).first()
	friends = user_friends.objects.filter(user=user).select_related('friend')
	if request.method == 'POST':
		search_query = request.POST.get('search_query', '').strip()
		if search_query:
			potential_friend = user_profile.objects.filter(login=search_query).first()
			if user.login == search_query:
				messages.error(request, 'You cannot add yourself as a friend.')
			elif potential_friend and potential_friend != user:
				if not user_friends.objects.filter(user=user, friend=potential_friend).exists():
					user_friends.objects.create(user=user, friend=potential_friend)
					messages.success(request, f"{potential_friend.login} added as friend.")
				else:
					messages.warning(request, "Already friends.")
			else:
				messages.error(request, "User not found.")

	context = {'friends': friends}
	return render(request, 'base.html', context)

def logout_view(request):
    logout(request)
    
    request.session.flush()

    return redirect('login')


