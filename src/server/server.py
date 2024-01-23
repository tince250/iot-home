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
    client.subscribe("topic/clock-alarm/server")

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
    else:
        # Handle messages from other topics
        print('nije tu')
        #save_to_db(json.loads(msg.payload.decode('utf-8')))


mqtt_client.on_connect = on_connect
# mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))
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
    print("alarm off")
    mqtt_client.publish("topic/clock-alarm/device/off", json.dumps({"action": "off"}))
    return jsonify({'message': f'Turn alarm off'})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001, use_reloader=False)
