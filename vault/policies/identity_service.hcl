path "django/identity/*" {
  capabilities = ["read", "list"]
}

path "database/identity/*" {
  capabilities = ["read", "list"]
}

path "redis/*" {
  capabilities = ["read", "list"]
}

path "aws/iam/*" {
  capabilities = ["read"]
}

path "aws/ses/smtp/*" {
  capabilities = ["read"]
}

path "transit/sign/jwt-rsa-key" {
  capabilities = ["update"]
}

path "transit/verify/jwt-rsa-key" {
  capabilities = ["read"]
}