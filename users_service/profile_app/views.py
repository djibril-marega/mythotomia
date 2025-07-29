from django.shortcuts import render, redirect
import os
from auth_manage.verify_jwt import verify_jwt_ps256_with_vault_key, validate_playload
from auth_manage.connection import connect_to_vault 
from django.conf import settings 
from .models import UserProfile
from .forms import ChangeProfile
from django.http import Http404  
from django.http import HttpResponseServerError
from django.http import JsonResponse
import unicodedata

def profile_edit_view(request):
    # Récupération du token
    token = request.COOKIES.get("access_token")
    if not token:
        return redirect('/authentification/login') 
    
    # Vérification du token
    vaultUrl = settings.VAULT_ADDR
    vaultToken = settings.VAULT_TOKEN 
    keyName = settings.VAULT_RSA_KEY_NAME
    
    try:
        client = connect_to_vault(vaultUrl, vaultToken)
        tokenIsVerified = verify_jwt_ps256_with_vault_key(client, token, keyName)
    except Exception as e:
        # En cas d'erreur de connexion à Vault
        print(f"Connection error to Vault: {e}")
        return HttpResponseServerError("Erreur interne du serveur.")
    
    if tokenIsVerified:
        tokenIsvalide = validate_playload(tokenIsVerified)
        if tokenIsvalide:
            try:
                user_profile = UserProfile.objects.get(external_user_id=tokenIsvalide["sub"])
            except UserProfile.DoesNotExist: 
                # Création du profil avec valeurs par défaut
                user_profile = UserProfile.objects.create(
                    external_user_id=tokenIsvalide["sub"], 
                    email=tokenIsvalide["email"],
                    username=tokenIsvalide["username"],
                    banner='banners/default-banner.jpg',
                    profile_photo='profiles/default-photo.png'
                )

            if request.method == "POST":
                form = ChangeProfile(request.POST, request.FILES) 
                if form.is_valid():
                    # Mise à jour des champs texte
                    if form.cleaned_data['first_name']:
                        user_profile.first_name = form.cleaned_data['first_name']
                    if form.cleaned_data['last_name']:
                        user_profile.last_name = form.cleaned_data['last_name']
                    if form.cleaned_data['bio']:
                        user_profile.bio = form.cleaned_data['bio']
                    if form.cleaned_data['birth_date']:
                        user_profile.birth_date = form.cleaned_data['birth_date']
                    
                    # Gestion de la bannière
                    if form.cleaned_data['banner']:
                        # Supprimer l'ancienne bannière si ce n'est pas la valeur par défaut
                        if user_profile.banner and not user_profile.banner.name.startswith('banners/default-'):
                            try:
                                os.remove(user_profile.banner.path)
                            except (ValueError, OSError):
                                pass
                        
                        # Sauvegarder la nouvelle bannière
                        banner_file = form.cleaned_data['banner']
                        new_banner_name = f"{user_profile.external_user_id}__{banner_file.name}"
                        new_banner_name_ascii = unicodedata.normalize('NFKD', new_banner_name).encode('ascii', 'ignore').decode('ascii')
                        user_profile.banner.save(new_banner_name_ascii, banner_file, save=False)
                    
                    # Gestion de la photo de profil
                    if form.cleaned_data['photo']:
                        # Supprimer l'ancienne photo si ce n'est pas la valeur par défaut
                        if user_profile.profile_photo and not user_profile.profile_photo.name.startswith('profiles/default-'):
                            try:
                                os.remove(user_profile.profile_photo.path)
                            except (ValueError, OSError):
                                pass
                        
                        # Sauvegarder la nouvelle photo
                        photo_file = form.cleaned_data['photo']
                        new_photo_name = f"{user_profile.external_user_id}__{photo_file.name}"
                        new_photo_name_ascii = unicodedata.normalize('NFKD', new_photo_name).encode('ascii', 'ignore').decode('ascii')
                        user_profile.profile_photo.save(new_photo_name_ascii, photo_file, save=False)
                    
                    user_profile.save()
                    return redirect('profile', username=user_profile.username)
                else:
                    return render(request, "edit_profile.html", {"form": form, "user_profile": user_profile}) 
            else:
                # Pré-remplir le formulaire avec les valeurs actuelles
                form = ChangeProfile(initial={
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'bio': user_profile.bio,
                    'birth_date': user_profile.birth_date
                })

            return render(request, "edit_profile.html", {"form": form, "user_profile": user_profile})
    
    # Si le token n'est pas valide ou vérifié
    return redirect('/authentification/login')


def profile_view(request, username):
    # JWT token verification
    token = request.COOKIES.get("access_token")
    user_id = None
    is_owner = False
    
    if token:
        vaultUrl = settings.VAULT_ADDR
        vaultToken = settings.VAULT_TOKEN 
        keyName = settings.VAULT_RSA_KEY_NAME
        client = connect_to_vault(vaultUrl, vaultToken)
        tokenIsVerified = verify_jwt_ps256_with_vault_key(client, token, keyName)
        
        if tokenIsVerified:
            tokenIsvalide = validate_playload(tokenIsVerified)
            if tokenIsvalide:
                user_id = tokenIsvalide["sub"]
    
    # Retrieving the profile 
    try:
        user_profile = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        # Create the profile if the user is authenticated and the username matches
        if user_id and username == tokenIsvalide.get("username", ""):
            user_profile = UserProfile.objects.create(
                external_user_id=user_id,
                email=tokenIsvalide["email"],
                username=username
            )
        else:
            raise Http404("Profil non trouvé")
    
    # # Check if the user is the owner of the profile
    if user_id and user_profile.external_user_id == user_id:
        is_owner = True
    
    context = {
        'user_profile': user_profile,
        'is_owner': is_owner,
        'show_birth_date': is_owner  # Only show the birth date if the viewer is the owner
    }
    
    return render(request, "profile.html", context)

def get_user_profile(request, user_id):
    try:
        profile = UserProfile.objects.get(external_user_id=user_id)
        
        # Construire l'URL publique via Nginx
        filename = profile.profile_photo.name.split('/')[-1]
        profile_picture_url = f"{settings.EXTERNAL_BASE_URL}/media/profiles/{filename}"
        
        return JsonResponse({
            'profile_picture': profile_picture_url,
            'username': profile.username,
            'first_name': profile.first_name, 
            'last_name': profile.last_name
        })
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)