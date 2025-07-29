output "instance_app_hostname" {
  description = "Public DNS name of the EC2 instance."
  value       = aws_instance.app_server.public_dns
}

output "instance_db_hostname" {
  description = "RDS instance hostname"
  value = aws_db_instance.database_postgresql.address
  sensitive = true
}

output "instance_db_password" {
  value = aws_db_instance.database_postgresql.password
  sensitive = true
}

output "instance_db_username" {
  value = aws_db_instance.database_postgresql.username
  sensitive = true
}