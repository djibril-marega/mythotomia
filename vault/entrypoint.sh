#!/bin/sh

# read UID and GID from the environment file 
VAULT_UID=$(grep 'vault_uid=' /uid_gid.env | cut -d= -f2)
VAULT_GID=$(grep 'vault_gid=' /uid_gid.env | cut -d= -f2)

if [ ! -f /vault/config/tls.crt ]; then
  echo "Generating TLS certificate..."
  openssl req -x509 -newkey rsa:4096 -sha256 -days 365 \
      -nodes -keyout /vault/config/tls-key.pem -out /vault/config/tls.crt \
      -subj "/CN=vault.local" \
      -addext "subjectAltName=DNS:vault,DNS:localhost,IP:127.0.0.1"
fi

# Ensure the vault directories exist and have the correct permissions 
chown -R $VAULT_UID:$VAULT_GID /vault/config
chown $VAULT_UID:$VAULT_GID /vault /vault/data
chown $VAULT_UID:$VAULT_GID /vault/config/tls*

exec su-exec $VAULT_UID:$VAULT_GID vault server -config=/vault/config/vault.hcl