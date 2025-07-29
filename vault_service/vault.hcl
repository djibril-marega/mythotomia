# Fichier vault.hcl
storage "raft" {
  path    = "/vault/data"
  node_id = "vault_node_1"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_cert_file = "/path/to/full-chain.pem"
  tls_key_file  = "/path/to/private-key.pem"
}

seal "awskms" {
  region     = "eu-west-1"
  kms_key_id = "ARN_DE_VOTRE_CLÉ_KMS"
}

api_addr     = "http://0.0.0.0:8200"
cluster_addr = "http://vault_node_1:8201"
ui           = true