import base64
import json
from .connection import connect_to_vault 
from django.conf import settings 
import hashlib

def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=') 

def create_unsigned_token(header, payload): 
    header_json = json.dumps(header, separators=(",", ":"), sort_keys=True).encode()
    payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    header_b64 = base64url_encode(header_json)
    payload_b64 = base64url_encode(payload_json)
    unsignedToken = b'.'.join([header_b64, payload_b64]).decode()
    return unsignedToken

def sign_token_with_vault(unsignedToken, RSAKeyName): # use other name key
    vaultUrl=settings.VAULT_ADDR 
    vaultToken=settings.VAULT_TOKEN
    client= connect_to_vault(vaultUrl, vaultToken)
    unsignedTokenHashBytes = hashlib.sha256(unsignedToken.encode()).digest()
    unsignedHTokenHashb64 = base64.b64encode(unsignedTokenHashBytes).decode()
    result = client.secrets.transit.sign_data(
        name=RSAKeyName,
        hash_input=unsignedHTokenHashb64, 
        key_version=None,
        prehashed=True,
        signature_algorithm='pss'
    )
    signature = result['data']['signature'].split(':')[-1] 
    signature_bytes = base64.b64decode(signature)
    signature_base64url = base64url_encode(signature_bytes).decode()
    return f"{unsignedToken}.{signature_base64url}"

def generate_token(header, playload, RSAKeyName):
    unsignedToken=create_unsigned_token(header, playload)
    token=sign_token_with_vault(unsignedToken, RSAKeyName) # use other name key
    return token 

