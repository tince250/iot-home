from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import paho.mqtt.client as mqtt

app = Flask(__name__)

token = ""
org = "iot"
url = "http://localhost:8086"
bucket = "measurements"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)


mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

def on_connect(client: mqtt.Client, userdata: any, flags, result_code):
    print("Connected with result code "+str(result_code))
    client.subscribe("topic/dht/temperature")
    client.subscribe("topic/dht/humidity")

def save_to_db(data, verbose=False):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
    )
    write_api.write(bucket=bucket, org=org, record=point)
    if verbose:
        print("Got message: " + data)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
