import paho.mqtt.client as mqtt
from django_celery_results.models import TaskResult

import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from django.conf import settings
from django.http import HttpResponse

from bots.models import BotConfig


def broadcast_log(message):
    CHANNEL = "aiw"
    # HOST = "mqtt.eclipse.org"
    # HOST = "103.108.140.185"

    HOST = "techcomengine.com"

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(CHANNEL)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print("message")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(HOST, 1883, 60)

    payload = message

    client.publish(CHANNEL, payload=payload, qos=1, retain=False)

    return True

def task_results_query():
    result = TaskResult.objects.all()
    for r in result:
        print(r.task_name)
        print(r.status)

    print(result)


def email_results():
    base_dir = settings.BASE_DIR

    try:
        email_setting = BotConfig.objects.get(config_class='email_results', config_validity=True)
        toaddr = email_setting.config_settings
    except (BotConfig.MultipleObjectsReturned, BotConfig.DoesNotExist) as e:
        toaddr = 'rkabir.rashed@gmail.com'
        print(e)

    me = 'ferntechaiw@gmail.com'
    subject = "The process is completed"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = toaddr
    msg.preamble = "test "
    # msg.attach(MIMEText(text))
    # attachment
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(os.path.join(base_dir, 'bank_asia_bots/final_info/final_status.csv'), "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="final_status.csv"')
    msg.attach(part)

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(user=me, password="woskxn29")

        s.sendmail(me, toaddr, msg.as_string())
        s.quit()
    # except:
    #   print ("Error: unable to send email")
    except smtplib.SMTPException as error:
        print("Error")

    return HttpResponse('done')
