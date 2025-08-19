api_addr = "https://vault:8200"
cluster_addr = "https://vault:8201"
cluster_name = "vault-cluster"
disable_mlock = true 
ui = true

seal "awskms" {
  region = "eu-west-3"
  kms_key_id = "arn:aws:kms:eu-west-3:888342500677:key/42535d26-61fd-4ee0-a2bc-71305f057150"
}
listener "tcp" {
  address = "0.0.0.0:8200"
  #cluster_address = "0.0.0.0:8201"
  tls_cert_file = "/vault/config/tls.crt"
  tls_key_file = "/vault/config/tls-key.pem"
  #tls_disable_client_certs = true
}

storage "raft" {
  path = "/vault/data"
  node_id = "vault-node-1"
}
