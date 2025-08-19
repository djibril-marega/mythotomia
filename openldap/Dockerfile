FROM bitnami/openldap:latest

COPY ./admin_policies.acl /tmp/admin_policies.acl
COPY ./add_users_policies.sh /opt/bitnami/openldap/conf/add_users_policies.sh
CMD [ "/opt/bitnami/openldap/conf/add_users_policies.sh" ]