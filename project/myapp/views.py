from django.shortcuts import render #http://157.245.40.149:30655
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .models import user_profile, match_record, user_friends
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import UserProfileForm
from django.contrib import messages
from django.utils import translation
from django.views.i18n import set_language
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import requests

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

def authorize(request):
    client_id = "client_id=u-s4t2ud-53a3167e09d6ecdd47402154ef121f68ea10b4ec95f2cb099cf3d92e56a0c822"
    redirect_uri = f"http://{request.get_host()}/callback"
    authorization_url = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect('/home/')

def base(request):
    return render(request, 'base.html')

def login(request):
    if request.htmx:
        template_name = 'home.html'
    else:
        template_name = 'home_full.html'
    # Check if the user is already authenticated
    if request.method == 'GET':
        print(f"am heeree{request.user.is_authenticated}")
    if request.user.is_authenticated:
        return redirect(template_name)
    user_info = request.session.get('user_info')
    print(f"am heeree{user_info}")
    if user_info:
		# If already authenticated, redirect to home or dashboard
        return redirect(template_name)
    return render(request, 'login.html')

@authenticated_user
def index(request):
    return render(request, 'index.html')

@authenticated_user
def home(request):
    if request.htmx:
        template_name = 'home.html'
    else:
        template_name = 'home_full.html'
    user = user_profile.objects.filter(login=request.session['user_info'].get('login')).first()
    return render(request, template_name, {'user':user})

@authenticated_user
def game(request):
    if request.htmx:
        template_name = 'home.html'
    else:
        template_name = 'home_full.html'
    user = user_profile.objects.filter(login=request.session['user_info'].get('login')).first()
    return render(request, template_name, {'user':user})

@authenticated_user
def friends(request):
    if request.htmx:
        template_name = 'friends.html'
    else:
        template_name = 'friends_full.html'
	
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
    return render(request, template_name, {'user':user})

@authenticated_user
def edit(request):
    if request.htmx:
        template_name = 'edit.html'
    else:
        template_name = 'edit_full.html'
    
    profile = user_profile.objects.filter(login=request.session['user_info'].get('login')).first()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save form data without committing to the database
            profile = form.save(commit=False)
            # Check if a new image was provided
            if 'image' in request.FILES:
                # Delete old image file
                if profile.image:
                    default_storage.delete(profile.image.path)
                # Save the new image file
                image = request.FILES['image']
                profile.image.save(image.name, ContentFile(image.read()))
                # Update the image_link field
                profile.image_link = profile.image.url
            # Save the profile to the database
            profile.save()
            return redirect('edit')
    else:
        form = UserProfileForm(instance=profile)
        form.fields['nickname'].widget.attrs.update({'class': 'form-control'})
    return render(request, template_name, {'form': form, 'user': profile})

@authenticated_user
def stats(request):
    if request.htmx:
        template_name = 'stats.html'
    else:
        template_name = 'stats_full.html'

    current_user_login = request.session['user_info'].get('login')
    # Use filter instead of get_object_or_404 to handle potential multiple profiles
    current_users = user_profile.objects.filter(login=current_user_login)
    # Handle the case where there are no matching profiles
    if not current_users.exists():
        return render(request, template_name, {'matches': [], 'match_count': 0})
    # Get the first profile if there are multiple matches (assuming login is unique)
    current_user = current_users.first()
    matches = match_record.objects.filter(Q(match_winner=current_user) | Q(match_loser=current_user))
    match_count = matches.count()
	# Calculate total wins, total losses, and success ratio
    total_wins = matches.filter(match_winner=current_user).count()
    total_losses = matches.filter(match_loser=current_user).count()
    success_ratio = total_wins / max(total_wins + total_losses, 1)
    return render(request, template_name, {'matches': matches, 'match_count': match_count, 'total_wins': total_wins, 'total_losses': total_losses, 'success_ratio': success_ratio, 'user': current_user})

@authenticated_user
def logout(request):
    # Revoke the OAuth2 token
    # if request.session.get('oauth_access_token'):
        # revoke_token * -> we need to revoke the token to logout
    request.session.clear()
    return redirect('login')

