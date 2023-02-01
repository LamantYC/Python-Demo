#!/usr/bin/env python
# coding:utf-8

import time
import json
import psutil
import random
from paho.mqtt import client as mqtt_client

broker = '120.48.78.39'
port = 1883
keepalive = 60
topic = "/python/mqtt"
client_id = f'python-mqtt-pub-{random.randint(0, 1000)}'


def to_M(n):
    u = 1024 * 1024
    m = round(n / u, 2)
    return m


def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    mem = psutil.virtual_memory()
    sdiskio = psutil.disk_io_counters()
    snetio = psutil.net_io_counters(pernic=True)
    mem_total, men_free = to_M(mem.total), to_M(mem.free)
    mem_percent = mem.percent
    info = {
        'cpu_percent': cpu_percent,  # 中央处理器百分比
        'cpu_count': cpu_count,  # 中央处理器计数
        'mem_total': mem_total,  # 内存总计
        'mem_percent': mem_percent,  # 内存百分比
        'read_count': sdiskio.read_count,  # 磁盘IO read_count
        'write_count': sdiskio.write_count,  # 磁盘IO write_count
        'read_bytes': sdiskio.read_bytes,  # 磁盘IO read_bytes
        'write_bytes': sdiskio.write_bytes,  # 磁盘IO write_bytes
        'read_time': sdiskio.read_time,  # 磁盘IO read_time
        'write_time': sdiskio.write_time,  # 磁盘IO write_time
        'snetio': snetio,  # 网卡信息
    }
    return json.dumps(info)


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("链接成功")
        else:
            print("连接失败，返回代码 %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port, keepalive)
    return client


def publish(client):
    while True:
        time.sleep(1)
        msg = get_system_info()
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"发送`{msg}`到主题`{topic}`")
        else:
            print(f"无法向主题发送消息{topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
