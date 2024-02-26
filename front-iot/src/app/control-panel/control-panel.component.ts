import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ApiService } from 'src/services/api.service';
import { ColorService } from 'src/services/color.service';

@Component({
  selector: 'app-control-panel',
  templateUrl: './control-panel.component.html',
  styleUrls: ['./control-panel.component.css']
})
export class ControlPanelComponent implements OnInit {
  controPanelGroup = new FormGroup({
    rgbColorSelect: new FormControl('', []),
    dmsCode: new FormControl('', []),
  })

  constructor(private apiService: ApiService, private colorService: ColorService) { }

  ngOnInit(): void {
    this.colorService.receivedColorUpdate().subscribe({
      next: (value) => {
        let color = value.toUpperCase();
        console.log(this.controPanelGroup.value.rgbColorSelect);
        if (color != this.controPanelGroup.value.rgbColorSelect)
          this.controPanelGroup.value.rgbColorSelect = color;
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

  sendDMSInput() {
    console.log(this.controPanelGroup.value.dmsCode)
    if (this.controPanelGroup.value.dmsCode) {
      this.apiService.sendDmsCode(this.controPanelGroup.value.dmsCode).subscribe({
        next: (value) => {
          console.log(value);
        },
        error(err) {
          console.log(err)
        },
      })
    }
  }
}
