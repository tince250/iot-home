import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { NavigationEnd, Router } from '@angular/router';
import { filter } from 'rxjs';
import { CreateClockAlarmDialogComponent } from '../create-clock-alarm-dialog/create-clock-alarm-dialog.component';
import { Socket } from 'ngx-socket-io';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css', '../pi1-dashboard/pi1-dashboard.component.css']
})
export class NavbarComponent {
  url = "/pi1";
  isAlarmOn: boolean = false;

  constructor(private router: Router,
    private dialog: MatDialog,
    private socket: Socket,
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
          this.isAlarmOn = true;
          break;
        case "off":
          this.isAlarmOn = false;
          break;
      }});
  }

  openCreateClockAlarmDialog() {
    this.dialog.open(CreateClockAlarmDialogComponent);
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
    this.http.put<any>(environment.apiGateway + "/clock-alarm/off", options).subscribe({
      next: (value: any) => {
        console.log(value);
      },
      error: (err) => {
        console.log(err);
      }
    });
  }
}
