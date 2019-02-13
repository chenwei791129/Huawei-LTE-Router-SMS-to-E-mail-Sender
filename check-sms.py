import os
import smtplib
import json
import time
import gettext

lang = {
    'zh_TW': "zh_TW",
    'zh_HK': "zh_HK",
    'zh_CN': "zh_CN",
    'en_US': "en_US",
}
SET_LANG = os.getenv("LOCALE")
CURRUNT_LOCALE = lang.get(SET_LANG, "en")
t = gettext.translation('messages', 'locale', [CURRUNT_LOCALE])
_ = t.gettext

# check if in docker
def runningInDocker():
    try:
        with open('/proc/self/cgroup', 'r') as procfile:
            for line in procfile:
                fields = line.strip().split('/')
                if fields[1] == 'docker':
                    return True
    except:
        pass
    return False

# Test and inatall the required module and load dotenv if not in docker
if not runningInDocker():
    try:
        import huawei_lte_api
    except ImportError:
        print(_('Trying to Install required module: huawei_lte_api'))
        os.system('pip install huawei_lte_api')
    try:
        import dotenv
    except ImportError:
        print(_('Trying to Install required module: python-dotenv'))
        os.system('pip install python-dotenv')
    from dotenv import load_dotenv
    load_dotenv()

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.Connection import Connection
from huawei_lte_api.api.User import User
from huawei_lte_api.enums.sms import BoxTypeEnum

# load environment variable from .env file
HUAWEI_ROUTER_IP_ADDRESS = os.getenv("HUAWEI_ROUTER_IP_ADDRESS")
HUAWEI_ROUTER_ACCOUNT = os.getenv("HUAWEI_ROUTER_ACCOUNT")
HUAWEI_ROUTER_PASSWORD = os.getenv("HUAWEI_ROUTER_PASSWORD")
GMAIL_ACCOUNT = os.getenv("GMAIL_ACCOUNT")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
MAIL_RECIPIENT = os.getenv("MAIL_RECIPIENT").split(",")
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
        print(_('{Date} Find a new SMS ID:{Message_Index}! from {Phone_Number}').format(Date=sms['Messages']['Message']['Date'], Message_Index=sms['Messages']['Message']['Index'], Phone_Number=sms['Messages']['Message']['Phone']))

        # send e-mail
        msg = MIMEMultipart()
        msg['Subject'] = _('You have a message from {Phone_Number}').format(Phone_Number=sms['Messages']['Message']['Phone'])
        body = _('Message date:{Date}\r\nMessage content：\r\n {Content}').format(Date=sms['Messages']['Message']['Date'], Content=sms['Messages']['Message']['Content'])
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(GMAIL_ACCOUNT, GMAIL_PASSWORD)
            server.sendmail(GMAIL_ACCOUNT, MAIL_RECIPIENT, msg.as_string())
            server.quit()
            print(_('ID:{Message_Index} from {Phone_Number} was successfully sent!').format(Message_Index=sms['Messages']['Message']['Index'], Phone_Number=sms['Messages']['Message']['Phone']))
            # Set the SMS status was read
            client.sms.set_read(int(sms['Messages']['Message']['Index']))
            # Logout
            client.user.logout()
        except Exception as e:
            client.user.logout()
            print(_('ID:{Message_Index} from {Phone_Number} failed to send! \r\nError message:\r\n{error_msg}').format(Message_Index=sms['Messages']['Message']['Index'], Phone_Number=sms['Messages']['Message']['Phone'], error_msg=e))
    except Exception as e:
        print(_('Router connection failed! Please check the settings. \r\nError message:\r\n{error_msg}').format(error_msg=e))
