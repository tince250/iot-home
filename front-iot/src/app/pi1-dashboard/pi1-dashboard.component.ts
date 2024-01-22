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

  constructor(private socket: Socket) {
  }

  ngOnInit(): void {
    this.socket.on('update/PI1', (data: any) => {
      data = JSON.parse(data);
      console.log(data)
      switch (data["name"]) {
        case "Room DHT1" :
          this.updateDHT(data, this.dht1);
          break;
        case "Room DHT2" :
          this.updateDHT(data, this.dht2);
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
  update_front: boolean
}