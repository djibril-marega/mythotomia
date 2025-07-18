import hvac 

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