from django.shortcuts import render
from auth_manage.verify_jwt import verify_jwt_ps256_with_vault_key, validate_playload
from auth_manage.connection import connect_to_vault 
from django.conf import settings 
from django.http import JsonResponse
from cryptography.hazmat.primitives import serialization 
from cryptography.hazmat.backends import default_backend 

# Create your views here.
def profile_edit_view(request):
    print("Voici la requête :", request)
    # get token
    token = request.COOKIES.get("access_token")
    if not token:
        return JsonResponse({"error": "Token manquant"}, status=401)
    
    print("Voici le token :", token, 'terminer') 
    # décoder le token 
    vaultUrl=settings.VAULT_ADDR
    vaultToken=settings.VAULT_TOKEN 
    keyName=settings.VAULT_RSA_KEY_NAME
    client=connect_to_vault(vaultUrl, vaultToken)
    tokenIsVerified=verify_jwt_ps256_with_vault_key(client, token, keyName)
    print("Token est vérifié : ", tokenIsVerified) 
    if tokenIsVerified:
        tokenIsvalide=validate_playload(tokenIsVerified)
        print("Token est validé : ", tokenIsvalide) 
    # vérifier si le profil de l'utilisateur de la requête correspond à celui du token
    # si il ne correspondent pas aller à la page de connexion
    # ---- fin de la requête pour les utilisateurs étrangers ---- continuer pour les utilisateurs propriétaire -----
    if request.method == "POST":
        # si ils corresspondent afficher la page avec les informations de l'utilisateur
        # 
        pass 


    return render(request, "edit_page.html")  

def profile_view(request):
    # récupérer le token dans la requête
    authHeader = request.headers.get('Authorization') 
    # décoder le token 
    # vérifier si le profil de l'utilisateur de la requête correspond à celui du token
    # si l'utilisateur du token et de la requête ne correspondent pas, renvoyer les infos disponible du profile ormis la date de naissance
    # ---- fin de la requête pour les utilisateurs étrangers ---- continuer pour les utilisateurs propriétaire -----

    # si l'utilisateur du token et de la requête correspondent, vérifier si il existe dans la base de donner 
    # s'il n'existe pas créer lui un profil par défaut // si il existe continuer 
    # renvoyer les informations complet du profil (profil + date de naissance)
    pass 
