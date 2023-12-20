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
        client_id = "u-s4t2ud-8156fc58fc2005216ad58258e48c1a311ceb0c4b4bd45451aba59272720501f4"
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
                # storing data of usere in object
                user_data.objects.create(
                    login = user_info.get('login'),
                    nickname = user_info.get('displayname'),
                    email = user_info.get('email'),
                    # image_link = data["image"]["link"]
                ).save()
                return render(request, 'home.html', {'user_info': user_info})
            else:
                return render(request, 'error.html', {'error': 'Access token not found in the response'})
        except requests.exceptions.RequestException as e:
            return HttpResponseServerError(f"An error occurred: {e}")
    else:
        return render(request, 'error.html', {'error': 'Authorization code is missing'})
