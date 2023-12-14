from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import paho.mqtt.client as mqtt

app = Flask(__name__)

token = "7HPyHiQ_zy7TDUrO7p-i1POQsIt1ydQn-PZhUjnYzdKpPxn3jyaWdaWrQxuyO-glMHyfO9rp_mhh1vqJ2kMavA=="
org = "iot"
url = "http://localhost:8086"
bucket = "measurements"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)


mqtt_client = mqtt.Client()

def on_connect(client: mqtt.Client, userdata: any, flags, result_code):
    print("Connected with result code "+str(result_code))
    client.subscribe("topic/dht/temperature")
    client.subscribe("topic/dht/humidity")
    client.subscribe("topic/button/press")
    client.subscribe("topic/buzzer/sound")
    client.subscribe("topic/pir/move")

def save_to_db(data, verbose=True):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    try:
        point = (
            Point(data["measurement"])
            .tag("simulated", data["simulated"])
            .tag("runs_on", data["runs_on"])
            .tag("name", data["name"])
            .field(data["field"], data["value"])
        )
        write_api.write(bucket=data["bucket"], org=org, record=point)
        if verbose:
            print("Got message: " + json.dumps(data))
    except:
        pass

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))

mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
