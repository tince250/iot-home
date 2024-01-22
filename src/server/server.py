from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import paho.mqtt.client as mqtt
# from env import INFLUXDB_TOKEN
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
    client.subscribe("topic/doorlight/toggle")
    client.subscribe("topic/uds/distance")
    client.subscribe("topic/ms/key-pressed")
    client.subscribe("topic/bir/button")
    client.subscribe("topic/gyro/angles")
    client.subscribe("topic/rgbdiode/status")

def get_gyro_point(data):
    return (
                Point(data["measurement"])
                .tag("simulated", data["simulated"])
                .tag("runs_on", data["runs_on"])
                .tag("name", data["name"])
                .tag("axis", data["axis"])
                .field(data["field"], data["value"])
            )

def save_to_db(data, verbose=True):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    try:
        if (data["measurement"] == "angle"):
            print("jeste")
            point = get_gyro_point(data)
        else:
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
    
    except Exception as e:
        print(str(e))
        pass

def on_receive(data):
    if data["name"] == "Door Motion Sensor 1" or data["name"] == "Door Motion Sensor 2":
        check_door_entrance(data["runs_on"])
    if "Room PIR" in data["name"]:
        with people_count_lock:
            if not people_count:
                print("ALARM!!!")
    save_to_db(data)

import threading
people_count = 0
people_count_lock = threading.Lock()

def check_door_entrance(runs_on):
    query = f'from(bucket: "measurements") |> range(start: -15s) |> filter(fn: (r) => r._measurement == "Distance" and r.runs_on == "{runs_on}")'

    result = influxdb_client.query_api().query(org=org, query=query)
    records = []

    for table in result:
        for record in table.records:
            records.append((record.get_time(), record.get_value()))
    if len(records) < 2:
        return
    
    sorted_records = sorted(records, key=lambda record: record[0], reverse=True)
    sorted_records = sorted_records if len(sorted_records) < 3 else sorted_records[:3]
    entering_order = all(sorted_records[i][1] < sorted_records[i + 1][1] for i in range(len(sorted_records) - 1))
    exiting_order = all(sorted_records[i][1] > sorted_records[i + 1][1] for i in range(len(sorted_records) - 1))
    
    global people_count
    with people_count_lock:
        if entering_order:
            people_count += 1
            print(f"Someone entered the house. People count: {people_count}")
        elif exiting_order:
            people_count -= 1
            print(f"Someone left the house. People count: {people_count}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: on_receive(json.loads(msg.payload.decode('utf-8')))
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False, port=5001)
