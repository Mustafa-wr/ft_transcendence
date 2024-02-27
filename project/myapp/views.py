from django.shortcuts import render #http://157.245.40.149:30655
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseServerError
from django.template import loader
from .models import user_profile, match_record, user_friends, Create_match_record
from .models import user_profile, match_record, Game, Match_maker
from . import forms
from django.utils.translation import gettext as _, gettext_lazy as _
from django.utils.translation import get_language, activate, gettext
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserProfileForm
from django.contrib import messages
from django.utils import translation
from django.views.i18n import set_language
from django.contrib.auth import logout
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import secrets
from django.contrib.auth.decorators import login_required
import pyotp
from datetime import datetime, timedelta

import requests
import json

def authenticated_user(view_func):
	def wrapper(request, *args, **kwargs):
		user_info = request.session.get('user_info')
		if user_info:
			# User is authenticated, allow access to the view
			# if user_info.get('is_2fa_enabled'):
			# 	if user.is_2fa_enabled:
			# 		# User has 2FA enabled, redirect to 2FA verification page
			# 		return redirect('verify_2fa')
			return view_func(request, *args, **kwargs)
		else:
			print("not authenticated")
			# User is not authenticated, redirect to the login page
			return redirect('login')
	return wrapper

def organizer(request):
	profile = user_profile.objects.filter(login=request.session['user_info'].get('login')).first()
	print(f"user infooooo{profile}")
	if request.method == 'POST':
		is_2fa_enabled_value = request.POST.get('is_2fa_enabled') == 'enable'
		profile.is_2fa_enabled = is_2fa_enabled_value
		profile.save()
		return redirect('edit')
	return {
		'user': profile,
	}

@authenticated_user
def stats(request):
	is_home_page = False
	context = organizer(request)
	return render(request, 'base.html', context)

def base(request):
	return render(request, 'base.html')

def login(request):
	# Check if the user is already authenticated
	if request.user.is_authenticated:
		return redirect('/home')
	user_info = request.session.get('user_info')
	if user_info:
		# If already authenticated, redirect to home or dashboard
		return redirect('home')
	return render(request, 'login.html', )

    # Your login logic goes here...
    # If the login is successful and the user is authenticated:
    # Set the user_info in the session
    # request.session['user_info'] = user_info  # Replace with your authenticated user info

    # Then redirect to home or dashboard

@authenticated_user
def index(request):
    return render(request, 'index.html')

@authenticated_user
def doubles(request):
	return render(request, 'doubles.html')

@authenticated_user
def game(request):
    is_home_page = False
    is_game = True
    return render(request, 'game.html', {'is_home_page': is_home_page, 'is_game': is_game})

# @authenticated_user
# def pong(request):
# 	user = user_profile.objects.filter(login=request.session['user_info'].get('login')).first()
# 	return render(request, 'pong.html', {'user': user})

@authenticated_user
def pong(request):
	return render(request, 'pong.html')
		# if (Match_maker.objects.all().count() == 0):
		# 		Match_maker.objects.create()
		# if request.method == 'GET':
		# 	match_maker = Match_maker.objects.first()
		# 	match_maker.players.remove(user_profile.objects.filter(login=request.session['user_info'].get('login')).first())
		# 	match_maker.players.add(user_profile.objects.filter(login=request.session['user_info'].get('login')).first())
		# 	if (match_maker.players.count() > 1):
		# 		game_instance = Game()
		# 		game_instance.player_1 = match_maker.players.all().first()
		# 		match_maker.players.remove(game_instance.player_1)
		# 		game_instance.player_2 = match_maker.players.all().first()
		# 		match_maker.players.remove(game_instance.player_2)
		# 		template = loader.get_template('pong.html')
		# 		context = {
		# 			'game': game_instance,
		# 		}
		# 		return HttpResponse(template.render(context, request))
		# 	else:
		# 		return render(request, 'no_players.html')
		# else:
		# 	if request.method == 'POST':
		# 		data = json.loads(request.body)
		# 		match_record_instance = match_record()
		# 		match_record_instance.match_winner = user_profile.objects.filter(login=data['match_winner']).first()
		# 		match_record_instance.match_loser = user_profile.objects.filter(login=data['match_loser']).first()
		# 		match_record_instance.winner_score = data['winner_score']
		# 		match_record_instance.loser_score = data['loser_score']
		# 		match_record_instance.save()
		# 		# return JsonResponse({'status': 'success'})
		# 	return redirect('home')

def authorize(request):
    client_id = "client_id=u-s4t2ud-53a3167e09d6ecdd47402154ef121f68ea10b4ec95f2cb099cf3d92e56a0c822"
    redirect_uri = f"https://{request.get_host()}/callback"

    authorization_url = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri=https://127.0.0.1:8000/callback&response_type=code"

    return redirect('/home/')

@authenticated_user
def home(request):
	context = organizer(request)
	return render(request, 'base.html', context)

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')

@authenticated_user
def tournament(request):
	return render(request, 'tournament.html')

@authenticated_user
def friends(request):
	is_home_page = False
	user = user_profile.objects.filter(login=request.session['user_info'].get('login')).first()
	friends = user_friends.objects.filter(user=user).select_related('friend')
	if request.method == 'POST':
		if 'delete_friend_id' in request.POST:
			friend_id = request.POST.get('delete_friend_id')
			friend_to_delete = user_friends.objects.filter(id=friend_id, user=user).first()
			if friend_to_delete:
				friend_to_delete.delete()
				messages.success(request, f"{friend_to_delete.friend.login} has been removed from friends.")
			else:
				messages.error(request, "Friend could not be found.")
			return redirect('friends')
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
	temp = organizer(request)
	context = {
		'friends': friends,
		'user': user,
		'form': temp['form'],
		'matches': temp['matches'],
		'match_count': temp['match_count'],
		'total_wins': temp['total_wins'],
		'total_losses': temp['total_losses'],
		'success_ratio': temp['success_ratio'],
	}
	return render(request, 'base.html', context)

@authenticated_user
def logout(request):
    # Revoke the OAuth2 token
    # if request.session.get('oauth_access_token'):
        # revoke_token * -> we need to revoke the token to logout
    request.session.clear()
	
    return redirect('login')

@authenticated_user
def edit(request):
	is_game = False
	is_home_page = False
	profile = user_profile.objects.filter(login=request.session['user_info'].get('login')).first()
	if request.method == 'POST':
		is_2fa_enabled_value = request.POST.get('is_2fa_enabled') == 'enable'
		profile.is_2fa_enabled = is_2fa_enabled_value
		profile.save()
		return redirect('edit')
	tmp = organizer(request)
	context = {
		'user': profile,
	}
	return render(request, 'base.html', context)



# def verify_2fa(request):
# 	if request.method == 'POST':
# 		if 'user_info' in request.session:
# 			# user_instance, created = User.objects.get_or_create(username=request.session['user_info'].get('login'))
# 			user_info = request.session.get('user_info')
# 			user = user_profile.objects.get(login=user_info.get('login'))
# 			otp = request.POST.get('otp')
# 			print (f"otp is {otp}")

# 			try:
# 				totp_device = TOTPDevice.objects.filter(user=user.user, confirmed=True).first()
# 				print(f"totp_device: {totp_device}")
# 				print(f"verify_token: {totp_device.verify_token(otp) if totp_device else None}")

# 				if totp_device and totp_device.verify_token(otp):
# 					request.session['user_info'] = user_info
# 					login(request, user_instance)
# 					messages.success(request, 'Two-Factor Authentication успешно подтверждена.')
# 					return redirect('home')
# 				else:
# 					messages.error(request, 'Uncorect.')
# 					return HttpResponse('google.com')
# 			except TOTPDevice.DoesNotExist:
# 				messages.error(request, 'You dont have Two-Factor Authentication.')
# 				return redirect('home')
# 			except Exception as e:
# 				print(f"Exception: {str(e)}")
# 				return HttpResponseServerError("Internal Server Error ---->")
# 		else:
# 			messages.error(request, 'Session data missing. Please log in again.')
# 			return render(request, 'login.html')
# 	else:
# 		return render(request, 'error.html', {'error': 'Invalid request method'})

def verify_2fa(request):
	if request.method == 'POST':
		otp = request.POST.get('otp')
		print (f"otp is {otp}")
		username = request.session['user_info'].get('login')
		user = user_profile.objects.get(login=username)

		otp_secret = request.session['otp_secret_key']
		otp_valid_until = request.session['otp_valid_until']

		if otp_secret and otp_valid_until is not None:
			otp_valid_until = datetime.fromisoformat(otp_valid_until)

			if otp_valid_until > datetime.now():
				totp = pyotp.TOTP(otp_secret, interval=300)
				if totp.verify(otp):
					auth_login(request, user)

					del request.session['otp_secret_key']
					del request.session['otp_valid_until']

					return redirect('home')
				else:
					messages.error(request, 'Invalid code')
					logout(request)
					print("Invalid codeddddddddddddd")
					return redirect('logout_view')
			else:
				messages.error(request, 'Code expired')
				return redirect('logout_view')
		else:
			messages.error(request, 'Session data missing')
			return redirect('logout_view')
	else:
		return render(request, 'error.html', {'error': 'Invalid request method'})

