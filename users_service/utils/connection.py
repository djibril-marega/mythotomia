import hvac 
import boto3

#connect to vault
def connect_to_vault(vaultUrl, vaultToken):
    try:
        client = hvac.Client(url=vaultUrl, token=vaultToken)
        if client.is_authenticated():
            print("Connected to Vault")
            return client
        else:
            print("Failed to connect to Vault") 
            return None
    except Exception as e:
        print("Error connecting to Vault:", e) 
        return None 


# retrieve the secrets from Vault 
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

    
def created_ses_client(awsCreds): 
    if awsCreds is None:
        print("AWS credentials are not provided")
        return None
    accessKeyId=awsCreds['ACCESS_KEY_ID']
    if accessKeyId is None:
        print("AWS access key ID is not provided")
        return None
    secretAccessKey=awsCreds['SECRET_ACCESS_KEY']
    if secretAccessKey is None:
        print("AWS secret access key is not provided")
        return None
    try:
        ses_client = boto3.client('ses', region_name='us-east-1', aws_access_key_id=accessKeyId, aws_secret_access_key=secretAccessKey)
        return ses_client
    except Exception as e:
        print("Error connecting to AWS SES:", e) 
        return None

def establish_ses_connection(vaultUrl, vaultToken, pathSecret, mountPoint='secret'): 
    client = connect_to_vault(vaultUrl, vaultToken)
    awsCreds = get_secrets_in_vault(client, pathSecret, mountPoint) 
    ses_client = created_ses_client(awsCreds)
    return ses_client 