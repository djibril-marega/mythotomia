FROM hashicorp/vault:latest

RUN echo "vault_uid=$(id -u vault)" > /uid_gid.env && \
    echo "vault_gid=$(id -g vault)" >> /uid_gid.env
USER root 
RUN apk add --no-cache openssl tini 
WORKDIR /app 
COPY ./entrypoint.sh /entrypoint.sh
COPY ./update_tls_certificate.sh /update_tls_certificate.sh 
RUN chmod +x /entrypoint.sh /update_tls_certificate.sh 
ENTRYPOINT ["/entrypoint.sh"]