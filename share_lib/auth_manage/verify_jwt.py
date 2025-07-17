import jwt 
from jwt.exceptions import InvalidKeyError, DecodeError

def get_public_key(client, keyName, versionKey="latest_version"):
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



def verify_jwt_ps256(client, token: str, keyName, versionKey="latest_version"): 
    # get public key
    publicKey=get_public_key(client, keyName, versionKey)
    print("La clé public est : ")
    print(publicKey)

    # verify jwt  
    try:
        playload=jwt.decode(token, publicKey, algorithms=["PS256"])
    except InvalidKeyError:
        print("Error : This JWT could not be authenticated.") 
        return False
    except DecodeError as e:
        print("Invalid signature :", e)
        return False

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
    
    return playload
    
