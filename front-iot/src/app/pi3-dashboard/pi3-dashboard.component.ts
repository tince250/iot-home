import { ColorService } from './../../services/color.service';
import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { UpdateDTO } from '../pi1-dashboard/pi1-dashboard.component';
import { BuzzerService } from 'src/services/buzzer.service';

@Component({
  selector: 'app-pi3-dashboard',
  templateUrl: './pi3-dashboard.component.html',
  styleUrls: ['./pi3-dashboard.component.css',  '../pi1-dashboard/pi1-dashboard.component.css']
})
export class Pi3DashboardComponent {

  dht4: UpdateDTO[] = [];
  bb: UpdateDTO = {} as UpdateDTO;
  rpir4: UpdateDTO = {} as UpdateDTO;
  rgb: UpdateDTO = {} as UpdateDTO;

  constructor(private socket: Socket,
    private buzzerService: BuzzerService,
    private colorService: ColorService) {}

  ngOnInit(): void {
    this.buzzerService.receivedBedroomBuzzerUpdate().subscribe({
      next: (value) => {
        let buzzerData : UpdateDTO = value;
        if (this.bb.datetime != buzzerData.datetime)
          this.bb = buzzerData;
      },
      error(err) {
        console.log(err);
      },
    })
    this.socket.on('update/PI3', (data: any) => {
      data = JSON.parse(data);
      
      switch (data["name"]) {
        case "Room DHT4" :
          this.updateDHT(data, this.dht4);
          break;
        case "Room PIR4":
          this.rpir4 = data;
          break;
        case "Bedroom Buzzer":
          this.bb = data;
          break;
        case "Bedroom RGB diode":
          this.rgb = data;
          this.colorService.updateRgbColor(this.rgb.value);
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
