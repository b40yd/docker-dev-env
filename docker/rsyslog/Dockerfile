FROM alpine:latest

RUN apk add --no-cache bash rsyslog procps net-tools

EXPOSE 514

COPY rsyslog.conf /etc/rsyslog.conf
COPY docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["rsyslogd", "-n"]
