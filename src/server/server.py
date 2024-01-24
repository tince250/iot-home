from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import paho.mqtt.client as mqtt
# from env import INFLUXDB_TOKEN
from flask_cors import CORS

import time

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

def send_alarm_data_to_frontend(data):
    print("emitting ****************")
    try:
        socketio.emit('alarm', json.dumps(data))
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
    client.subscribe("topic/clock-alarm/server")

def check_gyro_alarms(data):
    allowed_angle_range = [-8.5, 8.5]
    if data["value"] < allowed_angle_range[0]:
        raise_alarm(data, message=f"Rotation per {data['axis']} axis is lower then {allowed_angle_range[0]} with value = {data['value']}")
    elif data["value"] > allowed_angle_range[1]:
        raise_alarm(data, message=f"Rotation per {data['axis']} axis is greater then {allowed_angle_range[1]} with value = {data['value']}")

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

        print("UPDATE FRONT")
        if data["update_front"]:
            print("DA")
            send_latest_data_to_frontend(data)
    
    except Exception as e:
        print(str(e))
        pass

def get_current_time():
    t = time.localtime()
    return time.strftime('%d.%m.%Y. %H:%M:%S', t)

def raise_alarm(data, message="", verbose=True):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    try:
        point = (
                Point("alarm")
                .tag("caused_by", data["name"])
                .tag("message", message)
                .field("status", "ON")
            ) 
        
        write_api.write(bucket="events", org=org, record=point)
        alarm_data = {
            "caused_by": data["name"],
            "message": message,
            "status": "ON",
            "timestamp": get_current_time()
        }
        if verbose:
            print("Sound the alarm")
        send_alarm_data_to_frontend(alarm_data)
        mqtt_client.publish("topic/alarm/buzzer/on", json.dumps(alarm_data))
    
    except Exception as e:
        print(str(e))
        pass

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

            
def on_message_callback(client, userdata, msg):
    print(f"Received message from topic: {msg.topic}")
    print(f"Message payload: {msg.payload.decode('utf-8')}")

    # Check the topic and take action accordingly
    if msg.topic == "topic/clock-alarm/server":
        data = json.loads(msg.payload.decode('utf-8'))
        try:
            socketio.emit('clock-alarm', json.dumps({"action": data["action"]}))
        except Exception as e:
            print(str(e))
    elif msg.topic == "topic/gyro/angles":
        check_gyro_alarms(json.loads(msg.payload.decode('utf-8')))
        save_to_db(json.loads(msg.payload.decode('utf-8')))
    else:         
        data = json.loads(msg.payload.decode('utf-8'))
        if data["name"] == "Door Motion Sensor 1" or data["name"] == "Door Motion Sensor 2":
            check_door_entrance(data["runs_on"])
        if "Room PIR" in data["name"]:
            with people_count_lock:
                if not people_count:
                    print("ALARM!!!")
        save_to_db(data)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: on_message_callback(client, userdata, msg)
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

@app.route('/clock-alarm', methods=['POST'])
def post_clock_alarm():
    data = request.get_json()  # Get JSON data from the request body
    date = data.get('params').get('date')
    time = data.get('params').get('time')
    mqtt_client.publish("topic/clock-alarm/device/on", json.dumps(data.get('params')))
    return jsonify({'message': f'Data received successfully. Date: {date}, Time: {time}'})

@app.route('/clock-alarm/off', methods=['PUT'])
def clock_alarm_off():
    data = request.get_json() 
    print("clock alarm off")
    mqtt_client.publish("topic/clock-alarm/device/off", json.dumps({"action": "off"}))
    return jsonify({'message': f'Turn clock alarm off'})

@app.route('/alarm/off', methods=['PUT'])
def alarm_off():
    data = request.get_json() 
    print("alarm off")
    #mqtt_client.publish("topic/clock-alarm/device/off", json.dumps({"action": "off"}))
    
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    try:
        point = (
                Point("alarm")
                .tag("caused_by", "web")
                .tag("message", "Alarms turned of by web app")
                .field("status", "OFF")
            ) 
        alarm_data = {
            "caused_by": "web",
            "message": "Alarms turned of by web app",
            "status": "OFF"
        }

        write_api.write(bucket="events", org=org, record=point)
        mqtt_client.publish("topic/alarm/buzzer/off", json.dumps(alarm_data))

        return jsonify({'message': f'SUCCESS'}), 200
    
    except Exception as e:
        print(str(e))
        pass
    
    return jsonify({'message': "ERROR"}), 400

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001, use_reloader=False)
