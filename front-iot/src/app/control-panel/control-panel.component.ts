import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ApiService } from 'src/services/api.service';
import { ColorService } from 'src/services/color.service';

@Component({
  selector: 'app-control-panel',
  templateUrl: './control-panel.component.html',
  styleUrls: ['./control-panel.component.css']
})
export class ControlPanelComponent implements OnInit {
  rgbColorSelect = new FormControl('',[]);

  constructor(private apiService: ApiService, private colorService: ColorService) { }

  ngOnInit(): void {
    this.colorService.receivedColorUpdate().subscribe({
      next: (value) => {
        let color = value.toUpperCase();
        console.log(this.rgbColorSelect.value);
        if (color != this.rgbColorSelect.value)
          this.rgbColorSelect.setValue(color);
      },
      error(err) {
        console.log(err);
      },
    })
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
