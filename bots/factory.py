import paho.mqtt.client as mqtt
from django_celery_results.models import TaskResult


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
