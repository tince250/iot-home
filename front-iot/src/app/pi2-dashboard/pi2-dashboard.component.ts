import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-pi2-dashboard',
  templateUrl: './pi2-dashboard.component.html',
  styleUrls: ['./pi2-dashboard.component.css', '../pi1-dashboard/pi1-dashboard.component.css']
})
export class Pi2DashboardComponent implements OnInit{
  
  constructor(private socket: Socket) {
  }

  ngOnInit(): void {
    this.socket.on('update/PI1', (data: any) => {
      data = JSON.parse(data);
      
      switch (data["name"]) {
        // case "Room DHT1" :
        //   this.updateDHT(data, this.dht1);
        //   break;
        // case "Room DHT2" :
        //   this.updateDHT(data, this.dht2);
        //   break;
        // case "Door Light":
        //   this.dl = data;
        //   break;
        // case "Door Ultrasonic Sensor":
        //   this.uds1 = data;
        //   break;
      }
      // Handle received data
      console.log('Received Socket.IO message:', data);
    });
  }
}
