import { ColorService } from './../../services/color.service';
import { ApiService } from './../../services/api.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import { filter } from 'rxjs';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css', '../pi1-dashboard/pi1-dashboard.component.css']
})
export class NavbarComponent {
  url = "/pi1";

  constructor(private router: Router, private apiService: ApiService, private colorService: ColorService) { }

  ngOnInit(): void {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      this.url = event.url;
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
