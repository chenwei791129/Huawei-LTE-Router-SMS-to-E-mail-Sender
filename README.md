# Huawei LTE Router SMS to E-mail Sender

The python script can help you read your sms from e-mail box.

Tested on:
* HUAWEI B525s-65a

if you success use for other huawei router, you can feedback for me.

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
```console
$ docker pull awei/huawei-lte-router-sms-to-email-sender
$ docker run -e HUAWEI_ROUTER_PASSWORD=<password> -e GMAIL_ACCOUNT=<gmail-account> -e GMAIL_PASSWORD=<gmail-password> -e MAIL_RECIPIENT user@gmail.com -d awei/huawei-lte-router-sms-to-email-sender
```
### Option Environment Variables
* `HUAWEI_ROUTER_PASSWORD` Huawei router login password (example: 123456)
* `GMAIL_ACCOUNT` gmail account for smtp login example: user@gmail.com
* `GMAIL_PASSWORD` gmail password for smtp login example: P@ssw0rd
* `MAIL_RECIPIENT` Comma separated recipient example: user1@livemail.tw,user2@gmail.com

### Option Environment Variables
* `HUAWEI_ROUTER_IP_ADDRESS` Huawei router IP address (default: 192.168.8.1)
* `HUAWEI_ROUTER_ACCOUNT` Huawei router login account (default: admin)
* `DELAY_SECOND` Waiting seconds for each check (default: 10)

## Related Projects

- [theskumar/python-dotenv](https://github.com/theskumar/python-dotenv)
- [Salamek/huawei-lte-api](https://github.com/Salamek/huawei-lte-api)

## License

The python script is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).
