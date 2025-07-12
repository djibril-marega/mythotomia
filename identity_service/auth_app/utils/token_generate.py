import base64
import json
from .connection import connect_to_vault 
from django.conf import settings 

def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=') 

def create_unsigned_token(header, payload): 
    header_b64 = base64url_encode(json.dumps(header).encode())
    payload_b64 = base64url_encode(json.dumps(payload).encode())
    unsignedToken = b'.'.join([header_b64, payload_b64]).decode()
    return unsignedToken 

def sign_token_with_vault(unsignedToken, RSAKeyName): # use other name key
    vaultUrl=settings.VAULT_ADDR 
    vaultToken=settings.VAULT_TOKEN
    client= connect_to_vault(vaultUrl, vaultToken)
    result = client.secrets.transit.sign_data(
        name=RSAKeyName,
        hash_input=base64.b64encode(unsignedToken.encode()).decode(),
        key_version=None,
        prehashed=False,
        signature_algorithm='pss'
    )
    signature = result['data']['signature'].split(':')[-1] 
    return f"{unsignedToken}.{base64url_encode(base64.b64decode(signature.encode())).decode()}" 

def generate_token(header, playload, RSAKeyName):
    unsignedToken=create_unsigned_token(header, playload)
    token=sign_token_with_vault(unsignedToken, RSAKeyName) # use other name key
    return token 

