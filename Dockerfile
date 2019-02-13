#
# Dockerfile for awei/huawei-lte-router-sms-to-email-sender
#

FROM python:3.7-alpine
LABEL MAINTAINER AwEi

ENV HUAWEI_ROUTER_IP_ADDRESS=192.168.8.1 \
    HUAWEI_ROUTER_ACCOUNT=admin \
    HUAWEI_ROUTER_PASSWORD=123456 \
    GMAIL_ACCOUNT=user@gmail.com \
    GMAIL_PASSWORD=P@ssw0rd \
    MAIL_RECIPIENT=user1@livemail.tw,user2@gmail.com \
    DELAY_SECOND=10 \
    LOCALE=en_US

WORKDIR /home

COPY check-sms.py check-sms.py
COPY locale locale

RUN pip install --no-cache-dir huawei_lte_api && \
    rm /home/locale/en/LC_MESSAGES/messages.pot && \
    rm /home/locale/en_US/LC_MESSAGES/messages.pot && \
    rm /home/locale/zh_CN/LC_MESSAGES/messages.pot && \
    rm /home/locale/zh_HK/LC_MESSAGES/messages.pot && \
    rm /home/locale/zh_TW/LC_MESSAGES/messages.pot

CMD ["python3","/home/check-sms.py"]
