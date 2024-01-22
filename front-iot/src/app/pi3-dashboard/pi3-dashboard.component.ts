import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { UpdateDTO } from '../pi1-dashboard/pi1-dashboard.component';

@Component({
  selector: 'app-pi3-dashboard',
  templateUrl: './pi3-dashboard.component.html',
  styleUrls: ['./pi3-dashboard.component.css',  '../pi1-dashboard/pi1-dashboard.component.css']
})
export class Pi3DashboardComponent {

  dht4: UpdateDTO[] = [];
  bb: UpdateDTO = {} as UpdateDTO;
  rpir4: UpdateDTO = {} as UpdateDTO;

  constructor(private socket: Socket) {
  }

  ngOnInit(): void {
    this.socket.on('update/PI1', (data: any) => {
      data = JSON.parse(data);
      
      switch (data["name"]) {
        case "Room DHT4" :
          this.updateDHT(data, this.dht4);
          break;
        case "Room PIR4":
          this.rpir4 = data;
          this.rpir4.time = new Date().toLocaleTimeString();
          break;
        case "Bedroom Buzzer":
          this.bb = data;
          this.bb.time = new Date().toLocaleTimeString();
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
