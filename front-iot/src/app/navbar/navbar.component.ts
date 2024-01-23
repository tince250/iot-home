import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { NavigationEnd, Router } from '@angular/router';
import { filter } from 'rxjs';
import { CreateClockAlarmDialogComponent } from '../create-clock-alarm-dialog/create-clock-alarm-dialog.component';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css', '../pi1-dashboard/pi1-dashboard.component.css']
})
export class NavbarComponent {
  url = "/pi1";

  constructor(private router: Router,
    private dialog: MatDialog,) { }

  ngOnInit(): void {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      this.url = event.url;
    });
  }

  openCreateClockAlarmDialog() {
    this.dialog.open(CreateClockAlarmDialogComponent);
  }
}
