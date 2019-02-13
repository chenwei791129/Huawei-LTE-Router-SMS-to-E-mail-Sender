#
# Dockerfile for awei/huawei-lte-router-sms-to-email-sender
#

FROM python:3.7-alpine
LABEL MAINTAINER AwEi

ENV HUAWEI_ROUTER_IP_ADDRESS 192.168.8.1 \
    HUAWEI_ROUTER_ACCOUNT admin \
    HUAWEI_ROUTER_PASSWORD 123456 \
    GMAIL_ACCOUNT user@gmail.com \
    GMAIL_PASSWORD P@ssw0rd \
    MAIL_RECIPIENT user1@livemail.tw,user2@gmail.com \
    DELAY_SECOND 10

COPY check-sms.py /home/check-sms.py

RUN pip install --no-cache-dir huawei_lte_api

CMD ["python3","/home/check-sms.py"]
