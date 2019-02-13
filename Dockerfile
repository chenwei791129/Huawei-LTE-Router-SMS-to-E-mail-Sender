#
# Dockerfile for awei/huawei-lte-router-sms-to-email-sender
#

FROM python:3.7-alpine
LABEL MAINTAINER AwEi

ENV HUAWEI_ROUTER_IP_ADDRESS 192.168.8.1
ENV HUAWEI_ROUTER_ACCOUNT admin
ENV HUAWEI_ROUTER_PASSWORD 123456
ENV GMAIL_ACCOUNT user@gmail.com
ENV GMAIL_PASSWORD P@ssw0rd
ENV MAIL_RECIPIENT user1@livemail.tw,user2@gmail.com
ENV DELAY_SECOND 10

WORKDIR /home

ADD check-sms.py /home/check-sms.py

RUN pip install huawei_lte_api

CMD ["python3","check-sms.py"]
