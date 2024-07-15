# -*-coding:utf-8-*-
import json
import paho.mqtt.client as mqtt
import os
import shortuuid
import sys
import threading

############################################################
# 변경 가능
serverIP = "192.168.0.7"
serverPort = 1883
############################################################
client = mqtt.Client()
ae = "ae_test"
container = "cnt_test"


def on_connect(c, userdata, flags, rc):
    print("connected: rc " + str(rc))

    if 0 == rc:
        c.subscribe("/oneM2M/resp/" + ae + "/Mobius2/json")


def on_subscribe(c, userdata, mid, granted_qos):
    sys.stdout.write("subscribed\r\n>")


def on_message(c, userdata, msg):
    response = json.loads(msg.payload)

    if "pc" in response and "m2m:cin" in response["pc"] and "con" in response["pc"]["m2m:cin"]:
        sys.stdout.write(response["pc"]["m2m:cin"]["con"] + "\r\n>")
    else:
        print("message error")


def connect():
    global client

    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    client.connect(serverIP, serverPort, 60)

    client.loop_forever()


def interruptThread():
    while True:
        # CR 제거
        pubData = sys.stdin.readline()[:-1]

        if "EXIT" == pubData:
            os._exit(0)
        elif (0 == len(pubData)):
            sys.stdout.write(">")
            sys.stdout.flush()
        else:
            client.publish("/oneM2M/req/" + ae + "/Mobius2/json",
                           json.dumps({
                               "m2m:rqp": {
                                   "op": 1,
                                   "fr": ae,
                                   "to": "/Mobius/" + ae + "/" + container,
                                   "rqi": shortuuid.ShortUUID().random(length=10),
                                   "pc": {
                                       "m2m:cin": {
                                           "con": pubData
                                       }
                                   },
                                   "ty": 4
                               }
                           })
                           )


if __name__ == "__main__":
    print("Enter \"EXIT\" to exit.")

    interrupt = threading.Thread(target=interruptThread)
    interrupt.start()

    connect()
