path "django/users/*" {
  capabilities = ["read", "list"]
}

path "database/users/*" {
  capabilities = ["read", "list"]
}

path "transit/verify/jwt-rsa-key" {
  capabilities = ["read"]
}