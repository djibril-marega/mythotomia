import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
import json
import time 

def base64url_decode(data):
    data = data.encode() if isinstance(data, str) else data
    rem = len(data) % 4
    if rem > 0:
        data += b'=' * (4 - rem)
    return base64.urlsafe_b64decode(data)

def get_public_key_from_vault(client, keyName, versionKey="latest_version"):
    try:
        # Read key metadata from Vault 
        key_response = client.secrets.transit.read_key(name=keyName)
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve key '{keyName}' from Vault: {e}")

    data = key_response.get("data")
    if not data:
        raise ValueError(f"No data found for key '{keyName}'.")

    # Handle latest version
    if versionKey == "latest_version":
        versionKey = str(data.get("latest_version"))
        if not versionKey:
            raise ValueError(f"Could not determine latest version of key '{keyName}'.")

    # Access the specific version of the key
    keys = data.get("keys", {})
    version_data = keys.get(str(versionKey))
    if not version_data:
        raise ValueError(f"Version '{versionKey}' does not exist for key '{keyName}'.")

    public_key = version_data.get("public_key")
    if not public_key:
        raise ValueError(
            f"Public key not available for version '{versionKey}' "
            f"of key '{keyName}'. Make sure the key is marked as exportable."
        )

    return public_key

def verify_jwt_ps256_with_vault_key(client, token, keyName):
    # Split JWT
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError:
        raise ValueError("Token format invalid (must be 3 parts)")

    # Reconstruct message
    message = f"{header_b64}.{payload_b64}".encode()

    # Decode signature
    signature = base64url_decode(signature_b64)

    # Get public key
    publicKeyPem = get_public_key_from_vault(client, keyName, versionKey="latest_version")

    # Convert PEM string to RSA public key object
    publicKey = serialization.load_pem_public_key(publicKeyPem.encode())

    # Verify signature using PSS + SHA256
    try:
        publicKey.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Signature is valid")
        payloadJson = base64url_decode(payload_b64).decode()
        return json.loads(payloadJson)
    except InvalidSignature:
        print("Signature verification failed")
        return False


def validate_playload(playload):
    try:
        playload['sub']
        playload['email']
        playload['username']
        playload['email_verified']
        playload['role']
        playload['exp']
        playload['iss']
        playload['iat']
    except KeyError:
        print("Error : Not all required payload parameters are present.")
        return False
    
    now = int(time.time())
    if now > int(playload['exp']):
        print("Error : Token expired")
        return False
    
    return playload
    
