import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-pi1-dashboard',
  templateUrl: './pi1-dashboard.component.html',
  styleUrls: ['./pi1-dashboard.component.css']
})
export class Pi1DashboardComponent implements OnInit {

  dht1: UpdateDTO[] = [];
  dht2: UpdateDTO[] = [];
  dl: UpdateDTO = {} as UpdateDTO;
  uds1: UpdateDTO = {} as UpdateDTO;
  rpir1: UpdateDTO = {} as UpdateDTO;
  rpir2: UpdateDTO = {} as UpdateDTO;
  dpir1: UpdateDTO = {} as UpdateDTO;
  db: UpdateDTO = {} as UpdateDTO;
  ds1: UpdateDTO = {} as UpdateDTO;

  constructor(private socket: Socket) {
  }

  ngOnInit(): void {
    this.socket.on('update/PI1', (data: any) => {
      data = JSON.parse(data);
      
      switch (data["name"]) {
        case "Room DHT1" :
          this.updateDHT(data, this.dht1);
          break;
        case "Room DHT2" :
          this.updateDHT(data, this.dht2);
          break;
        case "Door Light":
          this.dl = data;
          this.dl.time = new Date().toLocaleTimeString();
          break;
        case "Door Ultrasonic Sensor":
          this.uds1 = data;
          this.uds1.time = new Date().toLocaleTimeString();
          break;
        case "Room PIR1":
          this.rpir1 = data;
          this.rpir1.time = new Date().toLocaleTimeString();
          break;
        case "Room PIR2":
          this.rpir2 = data;
          this.rpir2.time = new Date().toLocaleTimeString();
          break;
        case "Door Motion Sensor 1":
          this.dpir1 = data;
          this.dpir1.time = new Date().toLocaleTimeString();
          break;
        case "Door Buzzer":
          this.db = data;
          this.db.time = new Date().toLocaleTimeString();
          break;
        case "Door Sensor 1":
          this.ds1 = data;
          this.ds1.time = new Date().toLocaleTimeString();
          break;
      }
      // Handle received data
      console.log('Received Socket.IO message:', data);
    });
  }

  updateDHT(data: UpdateDTO, dht: UpdateDTO[]) {
    if (data["measurement"].toLowerCase() == "temperature") {
      dht[0] = data;
    } else {
      dht[1] = data;
    }
  }
}

export interface UpdateDTO {
  measurement: string,
  simulated: boolean,
  runs_on: string,
  name: string,
  value: string,
  field: string,
  bucket: string,
  update_front: boolean,
  time: string
}