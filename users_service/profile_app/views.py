from django.shortcuts import render
from auth_manage.verify_jwt import verify_jwt_ps256 
from auth_manage.connection import connect_to_vault 
from auth_manage.get_token import get_token_from_header 
from django.conf import settings 

# Create your views here.
def profile_edit_view(request):
    print("Voici la requête :", request)
    # récupérer le token dans la requête 
    
    token=get_token_from_header(request)
    print("Voici le token :", token) 
    # décoder le token 
    vaultUrl=settings.VAULT_ADDR
    vaultToken=settings.VAULT_TOKEN 
    keyName=settings.VAULT_RSA_KEY_NAME
    client=connect_to_vault(vaultUrl, vaultToken)
    tokenIsValid=verify_jwt_ps256(client, token, keyName, versionKey="latest_version")
    print(tokenIsValid)
    if tokenIsValid:
        pass 
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
