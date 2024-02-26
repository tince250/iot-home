import { ColorService } from './../../services/color.service';
import { ApiService } from './../../services/api.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { NavigationEnd, Router } from '@angular/router';
import { filter } from 'rxjs';
import { CreateClockAlarmDialogComponent } from '../create-clock-alarm-dialog/create-clock-alarm-dialog.component';
import { Socket } from 'ngx-socket-io';
import { BuzzerService } from 'src/services/buzzer.service';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css', '../pi1-dashboard/pi1-dashboard.component.css']
})
export class NavbarComponent {
  url = "/pi1";
  isClockAlarmOn: boolean = false;
  isAlarmOn: boolean = false;

  constructor(private router: Router,
    private dialog: MatDialog,
    private socket: Socket,
    private buzzerService: BuzzerService,
    private apiService: ApiService, private colorService: ColorService,
    private http: HttpClient) { }

  ngOnInit(): void {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      this.url = event.url;
    });
    this.socket.on('clock-alarm', (data: any) => {
      data = JSON.parse(data);
      
      switch (data["action"]) {
        case "on" :
          this.isClockAlarmOn = true;
          break;
        case "off":
          this.isClockAlarmOn = false;
          break;
      }});
    this.socket.on('alarm', (data: any) => {
        data = JSON.parse(data);
        console.log('Received Socket.IO message:', data);
        if (data["status"] == "ON")
            this.isAlarmOn = true;
        else
            this.isAlarmOn = false;

      });
    this.socket.on('update/PI1', (data: any) => {
        data = JSON.parse(data);
        console.log('Received Socket.IO message:', data);
        if (data["name"] == "Door Buzzer") {
            this.buzzerService.updateDoorBuzzerStatus(data);
        }
      });
    this.socket.on('update/PI3', (data: any) => {
        data = JSON.parse(data);
        console.log('Received Socket.IO message:', data);
        if (data["name"] == "Bedroom Buzzer")
            this.buzzerService.updateBedroomBuzzerStatus(data);
      });
  }

  openCreateClockAlarmDialog() {
    this.dialog.open(CreateClockAlarmDialogComponent);
  }

  turnClockAlarmOff(){
    const environment = {
      production: false,
      apiGateway: 'http://localhost:5001', // Replace this with your API Gateway URL
    };
    const options: any = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      }),
    };
    this.http.put<any>(environment.apiGateway + "/clock-alarm/off", options).subscribe({
      next: (value: any) => {
        console.log(value);
      },
      error: (err) => {
        console.log(err);
      }
    });
  }

  turnAlarmOff(){
    const environment = {
      production: false,
      apiGateway: 'http://localhost:5001', // Replace this with your API Gateway URL
    };
    const options: any = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      }),
    };
    this.http.put<any>(environment.apiGateway + "/alarm/off", options).subscribe({
      next: (value: any) => {
        this.isAlarmOn = false;
      },
      error: (err) => {
        console.log(err);
      }
    });
  }

  onRgbSelectionChange(event: any): void {
    console.log('Selected value:', event.value);

    this.apiService.updateRgbColor(event.value).subscribe({
      next: (value) => {
        console.log(value);
      },
      error(err) {
        console.log(err)
      },
    })
  }

}
