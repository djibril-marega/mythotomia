# 📚 share-lib

`share-lib` est une bibliothèque Python facilitant la gestion de la connexion à HashiCorp Vault, l'extraction de secrets, et la vérification de tokens JWT (signés avec PS256). Elle est conçue pour être utilisée dans des projets nécessitant une gestion sécurisée des clés et une vérification fiable des identités.

---

## 🚀 Installation

Installez la librairie avec :

```bash
pip install git+https://<ton-repo>.git#egg=share-lib
```

Ou localement :

```bash
git clone https://<ton-repo>.git
cd share_lib
pip install -e .
```

---

## 🗂️ Structure du projet

```
share_lib/
├── auth_manage/
│   ├── connection.py       # Connexion sécurisée à Vault
│   ├── get_token.py        # Extraction du token JWT depuis les headers HTTP
│   ├── vault_manage.py     # Récupération sécurisée des secrets depuis Vault
│   └── verify_jwt.py       # Vérification des JWT via les clés publiques de Vault
├── setup.py                # Configuration setuptools
```

---

## 🔐 Fonctionnalités

### 🔌 Connexion à Vault

```python
from auth_manage.connection import connect_to_vault

client = connect_to_vault(vaultUrl="http://localhost:8200", vaultToken="s.vault-token")
```

---

### 📥 Extraction de token JWT depuis les headers HTTP

```python
from auth_manage.get_token import get_token_from_header

token = get_token_from_header(request)  # Fonctionne avec Flask/Django
```

---

### 📦 Récupération de secrets depuis Vault

```python
from auth_manage.vault_manage import get_secrets_in_vault

secrets = get_secrets_in_vault(client, pathSecret="monapp/credentials")
```

---

### 🔏 Vérification d’un token JWT signé avec PS256

```python
from auth_manage.verify_jwt import verify_jwt_ps256

payload = verify_jwt_ps256(client, token="eyJhbGciOiJQUzI1NiIs...", keyName="jwt-key-name")
```

Le JWT doit contenir les champs suivants :

- `sub`
- `email`
- `username`
- `email_verified`
- `role`
- `exp`
- `iss`
- `iat`

---

## ⚙️ Dépendances

Les dépendances sont gérées dans `setup.py` :

```python
install_requires=[
    "PyJWT==2.10.1",
    "cryptography==45.0.5"
]
```

**Note :** le module `hvac` est utilisé mais n'est pas encore listé. Il faut l’ajouter si tu veux inclure toutes les dépendances :

```bash
pip install hvac
```

---

## 🧪 Exemple complet

```python
from auth_manage.connection import connect_to_vault
from auth_manage.get_token import get_token_from_header
from auth_manage.vault_manage import get_secrets_in_vault
from auth_manage.verify_jwt import verify_jwt_ps256

# Connexion à Vault
client = connect_to_vault("http://localhost:8200", "s.vault-token")

# Simulation de requête avec headers
class DummyRequest:
    headers = {"Authorization": "Bearer your.jwt.token.here"}

request = DummyRequest()
token = get_token_from_header(request)

# Vérification du token
payload = verify_jwt_ps256(client, token, keyName="jwt-key")
print(payload)
```

---

## 🧑‍💻 Auteur

**Marega Djibril**  
GitHub : [djibril-marega](https://github.com/djibril-marega)

---

## 📌 TODO

- [ ] Ajouter des tests unitaires
- [ ] Ajouter la documentation Sphinx
