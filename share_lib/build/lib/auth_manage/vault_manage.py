import hvac 

def get_secrets_in_vault(client, pathSecret, mountPoint='secret'):
    if client is None:
        print("Client is not connected to Vault")
        return None
    if pathSecret is None:
        print("Path to secret is not provided")
        return None
    if not isinstance(pathSecret, str):
        print("Path to secret must be a string")
        return None 
    
    try:
        # Check if the secret exists
        client.secrets.kv.v2.read_secret_version(mount_point=mountPoint, path=pathSecret)
    except hvac.exceptions.InvalidRequest as e:
        print("Secret not found in Vault:", e)
        return None

    try:
        # Read the secret version from Vault
        creds = client.secrets.kv.v2.read_secret_version(mount_point=mountPoint, path=pathSecret)
        return creds['data']['data']
    except Exception as e:
        print("Error retrieving credentials from Vault:", e)
        return None