import os
import smtplib
import json
import time

# Test and inatall the required module
try:
    import huawei_lte_api
except ImportError:
    print('Trying to Install required module: huawei_lte_api\r\n')
    os.system('pip install huawei_lte_api')
try:
    import dotenv
except ImportError:
    print('Trying to Install required module: python-dotenv\r\n')
    os.system('pip install python-dotenv')

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.Connection import Connection
from huawei_lte_api.api.User import User
from huawei_lte_api.enums.sms import BoxTypeEnum
from dotenv import load_dotenv

# load environment variable from .env file
load_dotenv()
HUAWEI_ROUTER_IP_ADDRESS = os.getenv("HUAWEI_ROUTER_IP_ADDRESS")
HUAWEI_ROUTER_ACCOUNT = os.getenv("HUAWEI_ROUTER_ACCOUNT")
HUAWEI_ROUTER_PASSWORD = os.getenv("HUAWEI_ROUTER_PASSWORD")
GMAIL_ACCOUNT = os.getenv("GMAIL_ACCOUNT")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
MAIL_RECIPIENT = eval(os.getenv("MAIL_RECIPIENT"))
DELAY_SECOND = int(os.getenv("DELAY_SECOND"))

# Use infinite loop to check SMS
while True:
    try:
        # Establish a connection with authorized
        connection = AuthorizedConnection('http://{}:{}@{}/'.format(HUAWEI_ROUTER_ACCOUNT, HUAWEI_ROUTER_PASSWORD, HUAWEI_ROUTER_IP_ADDRESS))
        client = Client(connection)

        # get first SMS(unread priority)
        sms = client.sms.get_sms_list(1, BoxTypeEnum.LOCAL_INBOX, 1, 0, 0, 1)

        # Skip this loop if the SMS was read
        if int(sms['Messages']['Message']['Smstat']) == 1:
            # Logout
            client.user.logout()
            #Inspection interval(second)
            time.sleep(DELAY_SECOND)
            continue

        # Find a new SMS, go send e-mail！
        print('{} Find a new SMS ID:{}！ from {}'.format(sms['Messages']['Message']['Date'], sms['Messages']['Message']['Index'], sms['Messages']['Message']['Phone']))

        # send e-mail
        msg = MIMEMultipart()
        msg['Subject'] = '您有一則簡訊來自 %s' % sms['Messages']['Message']['Phone']
        body = '訊息日期： {}\r\n簡訊內容：\r\n {}'.format(sms['Messages']['Message']['Date'], sms['Messages']['Message']['Content'])
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(GMAIL_ACCOUNT, GMAIL_PASSWORD)
            server.sendmail(GMAIL_ACCOUNT, MAIL_RECIPIENT, msg.as_string())
            server.quit()
            print('ID:{} from {} was successfully sent！'.format(sms['Messages']['Message']['Index'], sms['Messages']['Message']['Phone']))
            # Set the SMS status was read
            client.sms.set_read(int(sms['Messages']['Message']['Index']))
            # Logout
            client.user.logout()
        except Exception as e:
            client.user.logout()
            print('ID:{} from {} failed to send！ \r\nError message：\r\n{}'.format(sms['Messages']['Message']['Index'], sms['Messages']['Message']['Phone'], e))
    except Exception as e:
        print('Router connection failed! Please check the settings. \r\nError message：\r\n{}'.format(e))
