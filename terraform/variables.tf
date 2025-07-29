variable "instance_name" {
  description = "Value of the EC2 instance's Name tag."
  type        = string
  default     = "backend-server"
}

variable "instance_type" {
  description = "The EC2 instance's type."
  type        = string
  default     = "t2.micro"
}

variable "db_username" {
  description = "data base username"
  type = string
  sensitive = true
}

variable "db_password" {
  description = "data base password"
  type = string 
  sensitive = true
}

variable "ssh_public_key" {
  description = "SSH public key for accessing the EC2 instances."
  type        = string
  
}