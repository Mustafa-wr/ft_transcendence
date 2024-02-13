import requests
from django.shortcuts import render
from django.http import HttpResponseServerError
from .models import user_profile
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django_otp.plugins.otp_totp.models import TOTPDevice
from email.mime.text import MIMEText
from django.conf import settings
from .views import verify_2fa
import smtplib


def callback(request):
	if 'code' in request.GET:
		code = request.GET.get('code')
		print(f"Received authorization code: {code}")

		token_url = "https://api.intra.42.fr/oauth/token"
		client_id = "u-s4t2ud-53a3167e09d6ecdd47402154ef121f68ea10b4ec95f2cb099cf3d92e56a0c822"
		client_secret = "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"
		redirect_uri = "https://127.0.0.1:8000/callback"

		data = {
			'grant_type': 'authorization_code',
			'client_id': client_id,
			'client_secret': client_secret,
			'code': code,
			'redirect_uri': redirect_uri,
		}

		try:
			response = requests.post(token_url, data=data)
			response.raise_for_status()
			token_data = response.json()

			if 'access_token' in token_data:
				token = token_data['access_token']
				print(f"Received access token: {token}")

				user_info_url = "https://api.intra.42.fr/v2/me"
				headers = {'Authorization': f'Bearer {token}'}
				user_response = requests.get(user_info_url, headers=headers)
				user_response.raise_for_status()
				user_info = user_response.json()
				print('---------> ', user_profile.objects.filter(login=user_info.get('login')))
				user_instance, created = User.objects.get_or_create(username=user_info.get('login'))
				if not user_profile.objects.filter(login=user_info.get('login')).exists():
					user_instance, created = User.objects.get_or_create(username=user_info.get('login'))
					user_profile.objects.create(
						user=user_instance,
						login=user_info.get('login'),
						nickname=user_info.get('displayname'),
						email=user_info.get('email'),
					).save()
					request.session['user_info'] = user_info
					user_info = user_response.json()
					return render(request, 'home.html', {'user_info': user_info})

				user = user_profile.objects.get(login=user_info.get('login'))
				if user.is_2fa_enabled:
					totp_device = TOTPDevice.objects.create(user=user.user, confirmed=True)
					totp_device.save()

					totp_code = totp_device.key
					print(f'TOTP Code: {totp_code}')
					msg = MIMEText(f'Code of confirmation 2FA: {totp_code}')
					msg['Subject'] = "Confirmation 2FA"
					msg['From'] = settings.EMAIL_HOST_USER
					msg['To'] = user.email
					print(user.email)
					# debuglevel = True
					mail = smtplib.SMTP(settings.EMAIL_HOST, 587)
					# mail.set_debuglevel(debuglevel)
					mail.starttls()
					mail.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
					mail.sendmail(settings.EMAIL_HOST_USER, user.email, msg.as_string())
					mail.quit()
					return render(request, '2fa.html', {'user_info': user_info, 'totp_device': totp_device})
				else:
					request.session['user_info'] = request.session['user_info']
					login(request, user.user)
					return render(request, 'home.html', {'user_info': user_info})
			else:
				return render(request, 'error.html', {'error': 'Access token not found in the response'})
		except requests.exceptions.RequestException as e:
			return HttpResponseServerError(f"An error occurred: {e}")
	else:
		return render(request, 'error.html', {'error': 'Authorization code is missing'})