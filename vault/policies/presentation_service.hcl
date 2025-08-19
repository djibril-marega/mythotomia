path "django/presentation/*" {
  capabilities = ["read", "list"]
}

path "database/presentation/*" {
  capabilities = ["read", "list"]
}

path "transit/verify/jwt-rsa-key" {
  capabilities = ["read"]
}