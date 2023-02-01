#!/usr/bin/env python
# coding:utf-8

import time
import random
from paho.mqtt import client as mqtt_client

broker = '120.48.78.39'
port = 1883
keepalive = 60
topic = "/python/mqtt"
client_id = f'python-mqtt-pub-{random.randint(0, 1000)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        client.subscribe(topic)
        if rc == 0:
            print("已连接到 MQTT 正常!")
        else:
            print("连接失败，返回代码 %d\n", rc)

    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        print(msg.payload)

    client = mqtt_client.Client(client_id)
    client.connect(broker, port, keepalive)
    client.on_connect = on_connect
    client.on_message = on_message
    return client


def publish(client):
    while True:
        time.sleep(1)
        msg = "msg"
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"发送 `{msg}` 到主题 `{topic}`")
        else:
            print(f"无法向主题发送消息 {topic}")


def run():
    client = connect_mqtt()
    client.loop_forever()
    # client.loop_start()
    # publish(client)


if __name__ == '__main__':
    run()
