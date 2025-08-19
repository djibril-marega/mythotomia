path "django/*" {
  capabilities = ["read", "list", "create", "update", "delete", "patch"]
}

path "database/*" {
  capabilities = ["read", "list", "create", "update", "delete", "patch"]
}

path "redis/*" {
  capabilities = ["read", "list", "create", "update", "delete", "patch"]
}

path "aws/iam/*" {
  capabilities = ["read", "list", "create", "update", "delete", "patch"]
}

path "aws/ses/smtp/*" {
  capabilities = ["read", "list", "create", "update", "delete", "patch"]
}

path "transit/*" {
  capabilities = ["read", "list", "create", "update", "delete"]
}

path "pki/*" {
  capabilities = ["read", "list", "create", "update", "delete"]
}
