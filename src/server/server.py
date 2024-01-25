from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import paho.mqtt.client as mqtt
# from env import INFLUXDB_TOKEN
from flask_cors import CORS
import threading
import time

dms_alarm_activation_code = "1234"
dms_alarm_deactivation_code = "4321"

dms_alarm_timeout = 10
dms_alarm_is_active = False

dms_pin_arrived_event = [threading.Event(), threading.Event()]
start_countdown_event = [threading.Event(), threading.Event()]
dms_alarm_ringing = [False, False]
dms_alarm_lock = threading.Lock()

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
        print("31")
        print(str(e))

def send_alarm_data_to_frontend(data):
    print("emitting ****************")
    try:
        socketio.emit('alarm', json.dumps(data))
    except Exception as e:
        print("39")
        print(str(e))

token = "7HPyHiQ_zy7TDUrO7p-i1POQsIt1ydQn-PZhUjnYzdKpPxn3jyaWdaWrQxuyO-glMHyfO9rp_mhh1vqJ2kMavA=="
org = "iot"
url = "http://localhost:8086"
bucket = "measurements"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)


mqtt_client = mqtt.Client()

def on_connect(client: mqtt.Client, userdata: any, flags, result_code):
    print("Connected with result code "+str(result_code))
    client.subscribe("topic/ms/code")
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
        print("109")
        print(str(e))
        pass

def get_current_time():
    t = time.localtime()
    return time.strftime('%d.%m.%Y. %H:%M:%S', t)

def turn_ds_alarm_off(sensor_name):
    with app.app_context():
        print("UGASEN ALARM")
        global last_press_ds2, is_ds1_alarm_on, is_ds2_alarm_on
        if sensor_name == "Door Sensor 1":
            is_ds1_alarm_on = False
        else:
            is_ds2_alarm_on = False
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
        try:
            point = (
                    Point("alarm")
                    .tag("caused_by", sensor_name)
                    .tag("message", "Alarms turned off by closing door")
                    .field("status", "OFF")
                ) 
            alarm_data = {
                "caused_by": sensor_name,
                "message": "Alarms turned off by closing door",
                "status": "OFF"
            }
            send_alarm_data_to_frontend({"status": "OFF"})

            write_api.write(bucket="events", org=org, record=point)
            mqtt_client.publish("topic/alarm/buzzer/off", json.dumps(alarm_data))

        except Exception as e:
            print(str(e))

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
        print("139")
        print(str(e))
        pass

import threading
people_count = 0
people_count_lock = threading.Lock()

def write_people_count(count_no, verbose=True):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    try:
        point = (
                Point("people_count")
                .field("count", count_no)
            ) 
        write_api.write(bucket="measurements", org=org, record=point)
        
    except Exception as e:
        print("160")
        print(str(e))
        pass

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
    print(sorted_records)
    sorted_records = sorted_records if len(sorted_records) < 3 else sorted_records[:3]
    entering_order = all(sorted_records[i][1] < sorted_records[i + 1][1] for i in range(len(sorted_records) - 1))
    exiting_order = all(sorted_records[i][1] > sorted_records[i + 1][1] for i in range(len(sorted_records) - 1))
    
    global people_count
    with people_count_lock:
        if entering_order:
            people_count += 1
            write_people_count(people_count)
            print(f"Someone entered the house. People count: {people_count}")
        elif exiting_order:
            if people_count == 0:
                return
            people_count -= 1
            write_people_count(people_count)
            print(f"Someone left the house. People count: {people_count}")

def wait_for_dms_event(indx: int):
    global dms_alarm_ringing, dms_pin_arrived_event, start_countdown_event, dms_alarm_timeout
    print(indx)
    while True:
        start_countdown_event[indx].wait()

        if not dms_pin_arrived_event[indx].wait(timeout=dms_alarm_timeout):
            print("DMS ALARM ON ****************")
            with dms_alarm_lock:
                dms_alarm_ringing[indx] = True
            raise_alarm({"name": "server"}, f"DMS pin not inputed within DS timeout, for DS{indx+1}.", True)
        else:
            print("DMS CODE ARRIVED ON TIME ****************")
            dms_pin_arrived_event[indx].clear()

        start_countdown_event[indx].clear()
            
def on_message_callback(client, userdata, msg):
    global dms_pin_arrived_event, start_countdown_event

    print(f"Received message from topic: {msg.topic}")
    print(f"Message payload: {msg.payload.decode('utf-8')}")


    # Check the topic and take action accordingly
    if msg.topic == "topic/ms/code":
        try:
            message = json.loads(msg.payload.decode('utf-8'))
            code = message["code"]
        except Exception as e:
            print(str(e))
            return
        
        process_dms_code_received(code)
        return
    if msg.topic == "topic/clock-alarm/server":
        data = json.loads(msg.payload.decode('utf-8'))
        try:
            socketio.emit('clock-alarm', json.dumps({"action": data["action"]}))
        except Exception as e:
            print("184")
            print(str(e))
    elif msg.topic == "topic/gyro/angles":
        check_gyro_alarms(json.loads(msg.payload.decode('utf-8')))
        save_to_db(json.loads(msg.payload.decode('utf-8')))
    elif msg.topic == "topic/button/press":
        data = json.loads(msg.payload.decode('utf-8'))
        global door_sensor_lock, last_press_ds1, last_press_ds2
        if data["name"] == "Door Sensor 1":
            with door_sensor_lock:
                if data["value"] == "open":
                    last_press_ds1 = time.time() 
                else:
                    last_press_ds1 = 0
                    if dms_alarm_is_active:
                        start_countdown_event[0].set()
        if data["name"] == "Door Sensor 2":
            with door_sensor_lock:
                if data["value"] == "open":
                    last_press_ds2 = time.time() 
                else:
                    last_press_ds2 = 0
                    if dms_alarm_is_active:
                        start_countdown_event[1].set()
        save_to_db(data)
    else:         
        data = json.loads(msg.payload.decode('utf-8'))
        if data["name"] == "Door Motion Sensor 1" or data["name"] == "Door Motion Sensor 2":
            check_door_entrance(data["runs_on"])
        if "Room PIR" in data["name"]:
            with people_count_lock:
                if not people_count:
                    print("ALARM!!!")
                    raise_alarm(data, message=f"Move was detected by {data['name']} but there is 0 people")
        save_to_db(data)

def turn_dms_alarm_off():
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    try:
        point = (
                Point("alarm")
                .tag("caused_by", "dms")
                .tag("message", "Alarms turned of by dms pin input")
                .field("status", "OFF")
            ) 
        alarm_data = {
            "caused_by": "dms",
            "message": "Alarms turned of dms pin input",
            "status": "OFF"
        }

        write_api.write(bucket="events", org=org, record=point)
        mqtt_client.publish("topic/alarm/buzzer/off", json.dumps(alarm_data))
        socketio.emit('alarm', json.dumps({"status": "OFF"}))

    except Exception as e:
        print(str(e))

def process_dms_code_received(code: str):
    global dms_alarm_activation_code, dms_alarm_is_active, dms_pin_arrived_event, dms_alarm_ringing

    if code == dms_alarm_activation_code and not dms_alarm_is_active:
        with dms_alarm_lock:
            print("DMS ALARM ACTIVATED **************")
            dms_alarm_is_active = True
    elif code == dms_alarm_deactivation_code:
        with dms_alarm_lock:
            dms_alarm_is_active = False
        print("DMS ALARM DEACTIVATED **************")
        if dms_alarm_ringing[0] or dms_alarm_ringing[1]:
            #TODO: na front posalji da prestane alarm
            print("DMS ALARM OFF **************")
            with dms_alarm_lock:
                dms_alarm_ringing[0] = False
                dms_alarm_ringing[1] = False
            turn_dms_alarm_off()
        else:
            dms_pin_arrived_event[0].set()
            dms_pin_arrived_event[1].set()

@app.route('/dms/code', methods=['PUT'])
def update_dms_code():
    global dms_alarm_activation_code, dms_alarm_is_active, dms_pin_arrived_event, dms_alarm_ringing
    try:
        data = request.get_json()
        code = data.get('code', None)

        if code is not None:
            print(f"Received code: {code}")

            process_dms_code_received(code)

            return jsonify({'message': 'Code updated successfully'}), 200
        else:
            return jsonify({'error': 'Code not provided'}), 400

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/rgb/color', methods=['PUT'])
def update_rgb_color():
    try:
        data = request.get_json()
        color = data.get('color', None)

        if color is not None:
            print(f"Received color: {color}")

            mqtt_message = {"color": color}
            mqtt_client.publish("topic/rgb/color", payload=json.dumps(mqtt_message))

            return jsonify({'message': 'Color updated successfully'}), 200
        else:
            return jsonify({'error': 'Color not provided'}), 400

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: on_message_callback(client, userdata, msg)
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()


door_sensor_lock = threading.Lock()
last_press_ds1 = 0
last_press_ds2 = 0
is_ds1_alarm_on = False
is_ds2_alarm_on = False

def door_sensor_update():
    global door_sensor_lock, last_press_ds1, last_press_ds2, is_ds1_alarm_on, is_ds2_alarm_on
    while True:
        time.sleep(1)
        with door_sensor_lock:
            if not last_press_ds1 and is_ds1_alarm_on:
                turn_ds_alarm_off(data["name"])
                print("neca")
            if last_press_ds1 and time.time() - last_press_ds1 > 5:
                data = {"name": "Door Sensor 1"}
                if not is_ds1_alarm_on:
                    raise_alarm(data, message=f"Door 1 has been opened for more than 5 seconds")
                is_ds1_alarm_on = True
        with door_sensor_lock:
            if not last_press_ds2 and is_ds2_alarm_on:
                print("neca2")
                turn_ds_alarm_off(data["name"])
            if last_press_ds2 and time.time() - last_press_ds2 > 5:
                data = {"name": "Door Sensor 2"}
                print("251")
                if not is_ds2_alarm_on:
                    raise_alarm(data, message=f"Door 2 has been opened for more than 5 seconds")
                is_ds2_alarm_on = True
                

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
    global dms_alarm_ringing, dms_alarm_is_active, door_sensor_lock, last_press_ds1, last_press_ds2

    with door_sensor_lock:
        last_press_ds1 = 0
        last_press_ds2 = 0
    
    data = request.get_json() 
    print("alarm off")
    
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

        if dms_alarm_ringing:
            dms_alarm_ringing[0] = False
            dms_alarm_ringing[1] = False
            dms_alarm_is_active = False
            print("DMS ALARM DEACTIVATED **************")
            print("DMS ALARM OFF **************")

        return jsonify({'message': f'SUCCESS'}), 200
    
    except Exception as e:
        print("293")
        print(str(e))
        pass
    
    return jsonify({'message': "ERROR"}), 400

if __name__ == '__main__':
    door_sensor_detection = threading.Thread(target=door_sensor_update)
    door_sensor_detection.daemon = True
    door_sensor_detection.start()

    dms_alarm_countdown_ds1 = threading.Thread(target=wait_for_dms_event, args=(0,))
    dms_alarm_countdown_ds1.daemon = True
    dms_alarm_countdown_ds1.start()

    dms_alarm_countdown_ds2 = threading.Thread(target=wait_for_dms_event, args=(1,))
    dms_alarm_countdown_ds2.daemon = True
    dms_alarm_countdown_ds2.start()


    socketio.run(app, debug=True, port=5001, use_reloader=False)
