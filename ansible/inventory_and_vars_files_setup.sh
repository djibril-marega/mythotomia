#!/bin/bash

# Retrieve Terraform outputs 
#outputsJSON=$(terraform output -json)
#if [ -z "$outputsJSON" ]; then
    #echo "JSON is empty"
    #exit 1
#fi
outputsJSON='{
  "instance_app_hostname": {
    "sensitive": false,
    "type": "string",
    "value": "ec2-35-180-62-186.eu-west-3.compute.amazonaws.com"
  },
  "instance_backend_hostname": {
    "sensitive": true,
    "type": "string",
    "value": "ip-10-0-1-196.eu-west-3.compute.internal"
  },
  "instance_db_hostname": {
    "sensitive": true,
    "type": "string",
    "value": "terraform-20250727220650766300000001.c3uaca4yyib9.eu-west-3.rds.amazonaws.com"
  },
  "instance_db_password": {
    "sensitive": true,
    "type": "string",
    "value": "xxyRfQie5EbLMj8xgxmQCJGm"
  },
  "instance_db_username": {
    "sensitive": true,
    "type": "string",
    "value": "admin_db"
  }
}'


# Extractation of outputs with jq 
appHostname=$(echo "$outputsJSON" | jq -r '.instance_app_hostname.value')
backendHostname=$(echo "$outputsJSON" | jq -r '.instance_backend_hostname.value')
dbHostname=$(echo "$outputsJSON" | jq -r '.instance_db_hostname.value')  
dbUsername=$(echo "$outputsJSON" | jq -r '.instance_db_username.value')
dbPassword=$(echo "$outputsJSON" | jq -r '.instance_db_password.value')

# Verfying if the file .vault_pass.txt exists 
vaultPassFile="$HOME/ansible/.vault_pass.txt"
if [ ! -f "$vaultPassFile" ]; then
  echo "$vaultPassFile file not found. Please create it with the vault password."
  exit 1
fi

# Creation of the hosts_vars directory if it does not exist 
mkdir -p hosts_vars

# Creation of the hosts_vars/webservers.yaml
cat <<EOF > hosts_vars/appservers.yaml
app_hostname: $appHostname 
app_username: ubuntu
EOF

# Retrives .env file variables
if [ ! -f .env ]; then
  echo ".env file not found. Please create it with the necessary variables."
  exit 1
fi
# Load environment variables from .env file
sudo dos2unix .env
set -a
source .env
set +a

# Creation of the database.yaml file with Ansible Vault
tmp_file=$(mktemp)
cat <<EOF > "$tmp_file"
db_username: "$dbUsername"
db_password: "$dbPassword"
db_hostname: "$dbHostname"
db_identity_db: "$DB_IDENTITY_DB"
db_identity_username: "$DB_IDENTITY_USERNAME"
db_identity_password: "$DB_IDENTITY_PASSWORD"
db_users_db: "$DB_USERS_DB"
db_users_username: "$DB_USERS_USERNAME"
db_users_password: "$DB_USERS_PASSWORD" 
EOF

# Encryption of the database.yaml file using Ansible Vault 
ansible-vault encrypt "$tmp_file" \
  --output hosts_vars/database.yaml \
  --vault-id dev@$vaultPassFile

# Check if the encryption was successful
if [ $? -ne 0 ]; then
  echo "Error during encryption. Please check your vault password and try again."
  rm -f "$tmp_file"
  exit 1
fi

# Cleanup of the temporary file
rm -f "$tmp_file"

mkdir -p inventory
# Creation of the inventory.ini file 
cat <<EOF > inventory/inventory.ini
[appservers]
$appHostname    ansible_user=ubuntu ansible_port=22

[backends]
$backendHostname    ansible_user=ubuntu   ansible_ssh_common_args='-o ProxyJump=ubuntu@$appHostname'
EOF

echo "Inventory and secrets files created successfully."
