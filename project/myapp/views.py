from django.shortcuts import render #http://157.245.40.149:30655
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseServerError, HttpResponseRedirect
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
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import secrets
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
import pyotp
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

import requests
import json

@permission_classes([IsAuthenticated])
def authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        user_info = request.session.get('user_info')
        is_2fa_verified = request.session.get('is_2fa_verified', False)

        if user_info and (is_2fa_verified):
            return view_func(request, *args, **kwargs)
        else:
            print("not authenticated")
            return redirect('login')

    return wrapper

def login(request):
	user_info = request.session.get('user_info')
	is_2fa_verified = request.session.get('is_2fa_verified', False)
	if user_info and is_2fa_verified:
		return redirect('home')
	print("Login view rendering login.html")
	return render(request, 'login.html', {'user_info': user_info, 'otp_required': False})

@authenticated_user
@permission_classes([IsAuthenticated])
def home(request):
    user_info = request.session.get('user_info')
    is_2fa_verified = request.session.get('is_2fa_verified', False)

    if not is_2fa_verified:
        return redirect('logout_view')

    context = organizer(request)
    return render(request, 'base.html', context)

def organizer(request):
	profile = user_profile.objects.filter(login=request.session['user_info'].get('login')).first()
	if request.method == 'POST':
		is_2fa_enabled_value = request.POST.get('is_2fa_enabled') == 'enable'
		profile.is_2fa_enabled = is_2fa_enabled_value
		profile.save()
		return redirect('edit')
	return {
		'user': profile,
	}
@authenticated_user
@permission_classes([IsAuthenticated])
def stats(request):
	is_home_page = False
	context = organizer(request)
	return render(request, 'base.html', context)

@permission_classes([IsAuthenticated])
def base(request):
	return render(request, 'base.html')

@authenticated_user
@permission_classes([IsAuthenticated])
def index(request):
    return render(request, 'index.html')

@authenticated_user
@permission_classes([IsAuthenticated])
def doubles(request):
	return render(request, 'doubles.html')

@authenticated_user
@permission_classes([IsAuthenticated])
def game(request):
    is_home_page = False
    is_game = True
    return render(request, 'game.html', {'is_home_page': is_home_page, 'is_game': is_game})

# @authenticated_user
# def pong(request):
# 	user = user_profile.objects.filter(login=request.session['user_info'].get('login')).first()
# 	return render(request, 'pong.html', {'user': user})

@authenticated_user
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def logout_view(request):
	logout(request)
	response = redirect('login')  # Redirect to login page after logout
	response.delete_cookie('sessionid')  # Delete sessionid cookie
	response.delete_cookie('csrftoken')  # Delete csrftoken cookie
	request.session.flush()
	request.session.clear()  # Clear session data
	request.session['is_2fa_verified'] = False
	return response

@authenticated_user
@permission_classes([IsAuthenticated])
def tournament(request):
	return render(request, 'tournament.html')

@authenticated_user
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def edit(request):
	is_game = False
	is_home_page = False
	profile = user_profile.objects.filter(login=request.session['user_info'].get('login')).first()
	user_info = request.session.get('user_info')
	is_2fa_verified = request.session.get('is_2fa_verified', False)

	if not is_2fa_verified:
		return redirect('logout_view')

	if request.method == 'POST':
		is_2fa_enabled_value = request.POST.get('is_2fa_enabled') == 'enable'
		profile.is_2fa_enabled = is_2fa_enabled_value
		profile.save()
		messages.success(request, "data saved")
		return redirect('edit')
	tmp = organizer(request)
	context = {
		'user': profile,
	}
	return render(request, 'base.html', context)



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

					request.session['is_2fa_verified'] = True

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

