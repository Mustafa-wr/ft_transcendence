import requests
from requests.auth import HTTPBasicAuth
from django.shortcuts import render
from django.http import HttpResponseServerError
from .models import user_data

def callback(request):
    if 'code' in request.GET:
        code = request.GET.get('code')
        print(f"Received authorization code: {code}")
        
        token_url = "https://api.intra.42.fr/oauth/token"
        client_id = "u-s4t2ud-53a3167e09d6ecdd47402154ef121f68ea10b4ec95f2cb099cf3d92e56a0c822"
        client_secret = "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"
        redirect_uri = "http://127.0.0.1:8000/callback"
        
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
                request.session['user_info'] = user_info
                # storing data of usere in object
                user_data.objects.create(
                    login = user_info.get('login'),
                    nickname = user_info.get('displayname'),
                    email = user_info.get('email'),
                    # image_link = data["image"]["link"]
                ).save()
                user_info = user_response.json()
                return render(request, 'home.html', {'user_info': user_info})
            else:
                return render(request, 'error.html', {'error': 'Access token not found in the response'})
        except requests.exceptions.RequestException as e:
            return HttpResponseServerError(f"An error occurred: {e}")
    else:
        return render(request, 'error.html', {'error': 'Authorization code is missing'})