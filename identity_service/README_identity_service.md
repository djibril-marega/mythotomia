# 🛡️ Identity Service – Mythotomia

Service Django de gestion des comptes utilisateurs avec authentification JWT (RS256), intégration Vault, et envoi sécurisé de mails.

---

## ✨ Résumé

`identity_service` est un microservice d'identité qui :

- Authentifie les utilisateurs via JWT RS256
- Permet l’inscription, la connexion, la déconnexion, la modification et la suppression de compte
- Vérifie les adresses e-mail avec un code à 6 chiffres
- Notifie les utilisateurs par mail après chaque action critique
- Supprime automatiquement les comptes désactivés après un délai de 30 jours
- Utilise Vault pour la gestion des secrets et la génération des clés RSA **sans jamais exposer la clé privée**

---

## ⚙️ Fonctionnalités principales

- 🔐 Authentification JWT signée avec RS256 (clé privée stockée dans Vault)
- 📧 Envoi d’e-mails via AWS SES (SMTP ou IAM)
- ✅ Vérification d’e-mail à l'inscription ou après modification
- 🗑️ Suppression différée des comptes (désactivation → suppression après 30 jours)
- 🔄 Mise à jour sécurisée de l'email, du mot de passe ou du nom d'utilisateur
- 📬 Notification par mail pour chaque action importante
- 🕒 Tâche périodique Celery (beat) pour supprimer les comptes expirés

---

## 🚀 Lancement local

### 🔁 Démarrage des services

Utilise `honcho` pour lancer tous les processus :

```bash
honcho start
```

Ce qui démarre :

- `web` : le serveur Django
- `worker` : le worker Celery
- `beat` : le planificateur de tâches périodiques

#### Exemples de `Procfile` :

procfile sur Windows
```
web: python manage.py runserver
worker: celery -A identity_service worker --pool=solo --loglevel=info
beat: celery -A identity_service beat --loglevel=info
```

procfile sur Linux
```
web: python manage.py runserver
worker: celery -A identity_service worker --loglevel=info
beat: celery -A identity_service beat --loglevel=info
```
---

## 🔐 Secrets gérés avec Vault

Tous les secrets nécessaires au fonctionnement du service sont stockés dans Vault. **La clé privée RSA utilisée pour signer les JWT est générée et utilisée directement depuis Vault sans jamais être extraite.**

---

## 📂 Variables d’environnement

Un fichier `.env.example` est fourni pour indiquer les clés attendues :

```env
# Enable or disable debug mode (true / false)
DEBUG=true

# Vault connection
VAULT_ADDR=http://127.0.0.1:8200
VAULT_TOKEN=hvs.xxxxxxxx (ne jamais versionner ce token)
MOUNT_POINT=service-identity

# Secret paths
SECRET_DB_PATH=db
SECRET_AWS_IAM_PATH=aws/ses/iam
SECRET_AWS_SMTP_PATH=aws/ses/smtp
SECRET_REDIS_PATH=redis
SECRET_DJANGO_PATH=django

# JWT key name
SECRET_RSA_KEY_NAME=jwt-rsa-key
```

🛑 **⚠️ Ne versionnez jamais votre token Vault !** En production, montez-le à runtime via une variable d’environnement ou un volume sécurisé. (voir ci-dessous)

---

## 🐳 Lancer avec Docker (optionnel)

### Build de l’image :

```bash
docker build -t identity-service .
```

### Lancer avec secrets montés (exemple CLI) :

```bash
docker run -d   --name identity   -p 8000:8000   -v /etc/secrets/vault_token:/run/secrets/vault_token:ro   -e VAULT_TOKEN_FILE=/run/secrets/vault_token   identity-service
```

---

## 🔧 Secrets requis dans Vault

Les secrets doivent être présents dans Vault avant le démarrage :

### 🔑 SMTP (pour envoyer les mails) :
```
SMTP_USERNAME
SMTP_PASSWORD
SMTP_EMAIL
```

### ☁️ IAM (aussi pour envoyer les mails (AWS SES)) :
```
ACCESS_KEY_ID
SECRET_ACCESS_KEY
```

### 🛢️ Base de données (PostgreSQL) :
```
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

### 🧠 Redis :
```
REDIS_PASSWORD
REDIS_SRV_IP
```

### ⚙️ Django :
```
DJANGO_SECRET_KEY
DJANGO_DEBUG
DJANGO_ALLOWED_HOSTS
```

---

## ⏱️ Tâches planifiées

Le service utilise Celery Beat pour planifier la suppression des comptes désactivés.

🎯 La planification de la tâche doit être configuré dans l’interface Django admin (`django-celery-beat`).

---

## 📦 Technologies utilisées

- Python 3.11
- Django 5.2
- Celery + Beat
- Redis
- Vault (HashiCorp)
- AWS SES (SMTP/IAM)
- JWT (RS256)
- Honcho

---

## 📚 Installation des dépendances

```bash
pip install -r requirements.txt
```

---

## 🔧 Dépendances

Avant de démarrer le service `identity_service`, assurez-vous que les services suivants sont disponibles et accessibles :

- **Vault** : utilisé pour gérer les secrets sensibles (clé RSA, mots de passe SMTP, etc.)
- **Redis** : utilisé comme broker pour Celery et Beat
- **PostgreSQL** : base de données principale de Django

**Ces services doivent être démarrés et configurés avant de lancer Django.**

Vous pouvez configurer les adresses/identifiants d'accès dans le fichier `.env` (voir `.env.example`).

---

### Ordre de démarrage conseillé

1. Vault
2. PostgreSQL
3. Redis
4. `identity_service` (avec `honcho start`)


## 🛠️ À faire

- [ ] Ajouter des tests automatisés
- [ ] Ajouter un service `user_profile` si séparation prévue 
- [ ] Ajouter une fonctionnalité de blacklist des tokens jwt révoquer dans le service identity (ex : à la déconnexion)
- [ ] Ajouter un uuid à chaque nouvel utilisateur dans le service identity et utiliser cela comme user id dans les tokens

---

## 📁 Projet parent : [Mythotomia](https://github.com/djibril-marega/mythotomia)

Ce service fait partie du projet global **Mythotomia**, actuellement en développement.

---

## 🧪 Exemple de test de connexion (token JWT RS256)

```bash
curl -X POST http://localhost:8000/api/login/      -H "Content-Type: application/json"      -d '{"email": "foo@bar.com", "password": "monmotdepasse"}'
```

Réponse :
```json
{
  "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 🛑 Sécurité

- 🔐 Le token JWT est signé côté serveur avec une **clé privée stockée dans Vault**.
- 🚫 Le token Vault **n’est jamais stocké dans l’image Docker**.
- ✅ Tous les secrets sont récupérés dynamiquement depuis Vault au runtime.

---

## ✍️ Auteur

Marega Djibril  
Projet personnel 
[GitHub : @djibril-marega](https://github.com/djibril-marega)
