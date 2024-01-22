from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import paho.mqtt.client as mqtt
from env import INFLUXDB_TOKEN
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
socketio = SocketIO(app, cors_allowed_origins="http://localhost:4200")

@socketio.on('connect')
def handle_connect():
    print('Client connected successfully\n')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected successfully\n')

def send_latest_data_to_frontend(data):
    print("emitting ****************")
    try:
        socketio.emit('update/' + data['runs_on'], json.dumps(data))
    except Exception as e:
        print(str(e))

token = INFLUXDB_TOKEN
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
    client.subscribe("topic/doorlight/toggle")
    client.subscribe("topic/uds/distance")
    client.subscribe("topic/ms/key-pressed")
    client.subscribe("topic/bir/button")

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

        if data["update_front"]:
            send_latest_data_to_frontend(data)
    except:
        pass

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
