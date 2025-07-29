#!/bin/sh

if [ ! -f /vault/config/tls.crt ]; then
  echo "Generating TLS certificate..."
  openssl req -x509 -nodes -newkey rsa:2048 \
      -keyout /vault/config/tls.key \
      -out /vault/config/tls.crt \
      -days 365 \
      -subj "/CN=http://vault:8200"
fi

exec vault server -config=/vault/config/vault.hcl
