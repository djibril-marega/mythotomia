FROM alpine:3.10

RUN apk add --no-cache \
	bash \
	tinyproxy

COPY ./tinyproxy.conf  /etc/tinyproxy/tinyproxy.conf

CMD ["tinyproxy", "-d"]