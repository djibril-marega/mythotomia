FROM vault:latest

USER root
RUN apk add --no-cache openssl

RUN mkdir -p /vault/config && \
    chown -R vault:vault /vault/config

COPY vault_config.hcl /vault/config/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
USER vault

ENTRYPOINT ["/entrypoint.sh"]