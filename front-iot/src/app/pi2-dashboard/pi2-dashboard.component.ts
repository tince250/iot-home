import { ApiService } from './../../services/api.service';
import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { UpdateDTO } from '../pi1-dashboard/pi1-dashboard.component';
import { BuzzerService } from 'src/services/buzzer.service';

@Component({
  selector: 'app-pi2-dashboard',
  templateUrl: './pi2-dashboard.component.html',
  styleUrls: ['./pi2-dashboard.component.css', '../pi1-dashboard/pi1-dashboard.component.css']
})
export class Pi2DashboardComponent implements OnInit{
  
  dht3: UpdateDTO[] = [];
  gdht: UpdateDTO[] = [];
  gyro: UpdateDTO[] = [];
  ds2: UpdateDTO = {} as UpdateDTO;
  rpir3: UpdateDTO = {} as UpdateDTO;
  dpir2: UpdateDTO = {} as UpdateDTO;
  dus2: UpdateDTO = {} as UpdateDTO;

  constructor(private socket: Socket,
    private buzzerService: BuzzerService) {
  }

  ngOnInit(): void {
    this.buzzerService.receivedDoorBuzzerUpdate().subscribe({
      next: (value) => {
        console.log(value);
        let buzzerData : UpdateDTO = value;
      },
      error(err) {
        console.log(err);
      },
    })
    this.socket.on('update/PI2', (data: any) => {
      data = JSON.parse(data);
      
      switch (data["name"]) {
        case "Room DHT3" :
          this.updateDHT(data, this.dht3);
          break;
        case "Garage DHT" :
          this.updateDHT(data, this.gdht);
          break;
        case "Door Sensor 2":
          this.ds2 = data;
          break;
        case "Door Motion Sensor 2":
            this.dpir2 = data;
            break;
        case "Room PIR3":
            this.rpir3 = data;
            break;
        case "Door Ultrasonic Sensor":
          this.dus2 = data;
          break
        case "Gun Safe Gyro":
          this.updateGyro(data);
          break
      }
      // Handle received data
      console.log('Received Socket.IO message:', data);
    });
  }

  updateGyro(data: UpdateDTO) {
    if (data["axis"] == "x") {
      this.gyro[0] = data;
    } else if (data["axis"] == "y") {
      this.gyro[1] = data;
    } else {
      this.gyro[2] = data;
    }
  }

  updateDHT(data: UpdateDTO, dht: UpdateDTO[]) {
    if (data["measurement"].toLowerCase() == "temperature") {
      dht[0] = data;
    } else {
      dht[1] = data;
    }
  }

}
