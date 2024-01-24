import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ColorService {

  public currentRgbColor = new Subject<string>();
  
  constructor() { }

  receivedColorUpdate() {
    return this.currentRgbColor.asObservable();
  }

  updateRgbColor(value: string) {
      this.currentRgbColor.next(value);
  }
}
