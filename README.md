# Huawei LTE Router SMS to E-mail Sender

The python script can help you read your sms from e-mail box.

Tested on:
* HUAWEI B525s-65a

if you success use for other huawei router, you can feedback for me.

## Operational content

1. Find the unread SMS
2. Send the SMS context via email
3. Set has been read status for this SMS
4. Loop to step 1

## How to use

1. copy .env.example to .env
```console
$ cp .env.example .env
$ vim .env
```

2. just run it!
```console
$ python3 check-sms.py
```

## Via Docker
[![This image on DockerHub](https://img.shields.io/docker/pulls/awei/huawei-lte-router-sms-to-email-sender.svg)](https://hub.docker.com/r/awei/huawei-lte-router-sms-to-email-sender/)

[View on Docker Hub](https://hub.docker.com/r/awei/huawei-lte-router-sms-to-email-sender)
```console
$ docker run -e HUAWEI_ROUTER_PASSWORD=<password> -e GMAIL_ACCOUNT=<gmail-account> -e GMAIL_PASSWORD=<gmail-password> -e MAIL_RECIPIENT=<your-email-address> -d awei/huawei-lte-router-sms-to-email-sender
```
### Necessary Environment Variables
* `HUAWEI_ROUTER_PASSWORD` Huawei router login password (example: 123456)
* `GMAIL_ACCOUNT` gmail account for smtp login (example: user@gmail.com)
* `GMAIL_PASSWORD` gmail password for smtp login (example: P@ssw0rd)
* `MAIL_RECIPIENT` Comma separated recipient (example: user1@livemail.tw,user2@gmail.com)

### Option Environment Variables
* `HUAWEI_ROUTER_IP_ADDRESS` Huawei router IP address (default: 192.168.8.1)
* `HUAWEI_ROUTER_ACCOUNT` Huawei router login account (default: admin)
* `DELAY_SECOND` Waiting seconds for each check (default: 10)
* `LOCALE` Set lang (default: en_US, support en_US, zh_TW, zh_HK, zh_CN)


## Related Projects

- [theskumar/python-dotenv](https://github.com/theskumar/python-dotenv) (used for non-docker environment)
- [Salamek/huawei-lte-api](https://github.com/Salamek/huawei-lte-api)

## License

The python script is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).
