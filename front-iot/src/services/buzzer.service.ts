import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';
import { UpdateDTO } from 'src/app/pi1-dashboard/pi1-dashboard.component';

@Injectable({
  providedIn: 'root'
})
export class BuzzerService {

  public bedroomBuzzerStatus = new BehaviorSubject<any>(null);
  public doorBuzzerStatus = new BehaviorSubject<any>(null);
  constructor() { }

  receivedBedroomBuzzerUpdate() {
    return this.bedroomBuzzerStatus.asObservable();
  }

  receivedDoorBuzzerUpdate() {
    return this.doorBuzzerStatus.asObservable();
  }

  updateDoorBuzzerStatus(value: UpdateDTO) {
    console.log("BUZZ NEXT")
      this.doorBuzzerStatus.next(value);
  }

  updateBedroomBuzzerStatus(value: UpdateDTO) {
    this.bedroomBuzzerStatus.next(value);
}
}