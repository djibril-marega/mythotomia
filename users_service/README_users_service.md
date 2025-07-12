# users_service

## ✨ Objectif

Gérer les profils utilisateurs : création, modification, consultation (privée/publique).

## 🔧 Fonctionnalités

- Modifier son profil : nom, prénom, bio, photo, bannière, date de naissance.
- Consulter son propre profil.
- Consulter le profil d’un autre utilisateur (données publiques seulement).
- Masquage optionnel de la date de naissance.
- Sécurité : un utilisateur ne peut modifier que son propre profil.

## 🔐 Sécurité

- L’utilisateur est identifié via un token JWT.
- Le token est vérifié par la gateway (`api_service`) avant d’arriver ici.
- Le `users_service` peut extraire les infos du token s’il a besoin de s’assurer de l’identité.

## 🛣️ Routes prévues

| Méthode | URL                  | Description                        |
|---------|----------------------|------------------------------------|
| GET     | `/profile/me/`       | Voir son profil complet            |
| GET     | `/profile/<id>/`     | Voir un autre profil (données publiques) |
| POST    | `/profile/me/edit/`  | Modifier son propre profil         |

## 🛠️ À faire

- [ ] Modèle de profil utilisateur
- [ ] Middleware ou fonction de vérification d'identité (api)
- [ ] Vues Django ou DRF pour les routes ci-dessus
