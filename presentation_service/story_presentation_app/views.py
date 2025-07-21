from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import PresentationStory
from .forms import PresentationStoryForm
from auth_manage.verify_jwt import verify_jwt_ps256_with_vault_key, validate_playload  # Correction orthographe
from auth_manage.connection import connect_to_vault
from django.conf import settings 
from django.http import HttpResponseServerError
import requests

@require_http_methods(["GET", "POST"])
def create_story_view(request):
    token = request.COOKIES.get("access_token")
    if not token:
        return redirect('/authentification/login') 
    
    vaultUrl = settings.VAULT_ADDR
    vaultToken = settings.VAULT_TOKEN 
    keyName = settings.VAULT_RSA_KEY_NAME
    
    try:
        client = connect_to_vault(vaultUrl, vaultToken)
        payload = verify_jwt_ps256_with_vault_key(client, token, keyName)
    except Exception as e:
        print(f"Erreur Vault: {e}")
        return HttpResponseServerError("Erreur interne du serveur.")
    
    if payload and validate_playload(payload):
        if request.method == 'POST':
            form = PresentationStoryForm(request.POST, request.FILES)
            if form.is_valid():
                story = form.save(commit=False)
                # Ajout des données utilisateur
                story.external_user_id = payload['sub']
                story.email = payload['email']
                story.username = payload['username']
                story.save()
                return redirect('story', id=story.id)
        else:
            form = PresentationStoryForm()
        
        return render(request, 'create_presentation_story.html', {'form': form})
    
    return redirect('/authentification/login')

def story_view(request, id):
    story = get_object_or_404(PresentationStory, id=id)
    profile_picture = None
    try:
        users_api_path = f"/profile/api/user/{story.external_user_id}/"
        response = requests.get(
            f"http://users:8000{users_api_path}",  # Nom du conteneur
            timeout=2,
            headers={'Host': 'localhost'} 
        )
        if response.status_code == 200:
            data = response.json()
            print("Voici les data :", data)
            profile_picture = data.get('profile_picture')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
    except requests.exceptions.RequestException:
        pass

    return render(request, 'presentation_story.html', {
        'story': story,
        'profile_picture': profile_picture,
        'first_name': first_name,
        'last_name': last_name 
    })