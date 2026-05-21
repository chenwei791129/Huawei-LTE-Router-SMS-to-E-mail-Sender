import gettext
import os
import signal
import smtplib
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import quote

import huawei_lte_api.exceptions
from dotenv import load_dotenv
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.Client import Client
from huawei_lte_api.enums.sms import BoxTypeEnum, SortTypeEnum

# Load .env when present (no-op inside Docker or when the file is absent)
load_dotenv()


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        sys.stderr.write("Missing required environment variable: {}\n".format(name))
        sys.exit(1)
    return value


def _handle_sigterm(signum, frame):
    sys.exit(128 + signum)


signal.signal(signal.SIGTERM, _handle_sigterm)

SET_LANG = os.getenv("LOCALE")
SUPPORTED_LOCALES = {"zh_TW", "zh_HK", "zh_CN", "en_US"}
CURRENT_LOCALE = SET_LANG if SET_LANG in SUPPORTED_LOCALES else "en"
t = gettext.translation("messages", "locale", [CURRENT_LOCALE])
_ = t.gettext

# load environment variables
HUAWEI_ROUTER_IP_ADDRESS = os.getenv("HUAWEI_ROUTER_IP_ADDRESS", "192.168.8.1")
HUAWEI_ROUTER_ACCOUNT = os.getenv("HUAWEI_ROUTER_ACCOUNT", "admin")
HUAWEI_ROUTER_PASSWORD = _required_env("HUAWEI_ROUTER_PASSWORD")
GMAIL_ACCOUNT = _required_env("GMAIL_ACCOUNT")
GMAIL_PASSWORD = _required_env("GMAIL_PASSWORD")
MAIL_RECIPIENT = _required_env("MAIL_RECIPIENT").split(",")
DELAY_SECOND = int(os.getenv("DELAY_SECOND", "10"))

connection = None
client: Client | None = None

# Use infinite loop to check SMS
try:
    while True:
        try:
            # Establish a connection with authorized.
            # URL-encode credentials so special chars (@, :, /, #, ?, %, space, ...) don't break urlparse.
            connection = AuthorizedConnection(
                "http://{}:{}@{}/".format(
                    quote(HUAWEI_ROUTER_ACCOUNT, safe=""),
                    quote(HUAWEI_ROUTER_PASSWORD, safe=""),
                    HUAWEI_ROUTER_IP_ADDRESS,
                )
            )
            client = Client(connection)

            # get first SMS(unread priority)
            sms = client.sms.get_sms_list(
                page=1,
                box_type=BoxTypeEnum.LOCAL_INBOX,
                read_count=1,
                sort_type=SortTypeEnum.DATE,
                ascending=False,
                unread_preferred=True,
            )

            # Skip this loop if no messages
            if sms["Messages"] is None:
                client.user.logout()
                continue

            # huawei-lte-api >=1.6.10 returns a list even for a single message
            message = sms["Messages"]["Message"][0]

            # Skip this loop if the SMS was read
            if int(message["Smstat"]) == 1:
                client.user.logout()
                continue

            # Find a new SMS, go send e-mail！
            print(_("{Date} Find a new SMS ID:{Message_Index}! from {Phone_Number}").format(Date=message["Date"], Message_Index=message["Index"], Phone_Number=message["Phone"]))

            # send e-mail
            msg = MIMEMultipart()
            msg["Subject"] = _("You have a message from {Phone_Number}").format(Phone_Number=message["Phone"])
            body = _("Message date:{Date}\nMessage content：\n {Content}").format(Date=message["Date"], Content=message["Content"])
            msg.attach(MIMEText(body, "plain"))

            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(GMAIL_ACCOUNT, GMAIL_PASSWORD)
                    server.sendmail(GMAIL_ACCOUNT, MAIL_RECIPIENT, msg.as_string())
                print(_("ID:{Message_Index} from {Phone_Number} was successfully sent!").format(Message_Index=message["Index"], Phone_Number=message["Phone"]))
                # Set the SMS status was read
                client.sms.set_read(int(message["Index"]))
            except Exception as send_err:
                print(
                    _("ID:{Message_Index} from {Phone_Number} failed to send! \nError message:\n{error_msg}").format(Message_Index=message["Index"], Phone_Number=message["Phone"], error_msg=send_err)
                )
            finally:
                try:
                    client.user.logout()
                except Exception:
                    pass
        except huawei_lte_api.exceptions.ResponseErrorLoginRequiredException:
            print(_("Session timeout, login again!"))
        except huawei_lte_api.exceptions.LoginErrorAlreadyLoginException:
            if client is not None:
                try:
                    client.user.logout()
                except Exception:
                    pass
        except Exception as e:
            print(_("Router connection failed! Please check the settings. \nError message:\n{error_msg}").format(error_msg=e))
        finally:
            # Inspection interval(second)
            time.sleep(DELAY_SECOND)
except KeyboardInterrupt:
    sys.exit(130)
