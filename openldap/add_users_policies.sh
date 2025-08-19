#!/bin/bash
# Script to configure OpenLDAP with admin policies
set -e

# Note: cn=module{1},cn=config assumes that the module will be loaded as the second module. cn=module{0} being the first.
# Additionally, olcDatabase={2}mdb assumes that the database is the second one configured in OpenLDAP. Adjust as necessary.

# Apply the LDIF file to the OpenLDAP configuration
echo "Applying admin policies to OpenLDAP configuration..."
echo "This will modify the access control policies for the OpenLDAP database." 
if [ -z "/tmp/admin_policies.acl" ]; then 
  echo  "Notice: The file /tmp/admin_policies.acl don't exist"
  exit 1
fi 

cat "/tmp/admin_policies.acl" >> "/opt/bitnami/openldap/etc/slapd.d/cn=config/olcDatabase={2}mdb.ldif"
echo "Admin user policies has been configured for database."
