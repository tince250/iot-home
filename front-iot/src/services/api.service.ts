import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  updateRgbColor(color: string): Observable<any> {
    const options: any = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      })
    };
    const endpoint = `${environment.apiHost}/rgb/color`;
    return this.http.put(endpoint, { color }, options);
  }
}
