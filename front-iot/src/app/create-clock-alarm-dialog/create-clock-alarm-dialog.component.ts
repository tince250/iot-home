import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { dateBeforeOfTodayValidator, timeFormatValidator, timePassedValidator } from 'src/validators/dateValidator';

@Component({
  selector: 'app-create-clock-alarm-dialog',
  templateUrl: './create-clock-alarm-dialog.component.html',
  styleUrls: ['./create-clock-alarm-dialog.component.css']
})
export class CreateClockAlarmDialogComponent implements OnInit{

  constructor(public dialogRef: MatDialogRef<CreateClockAlarmDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private snackBar: MatSnackBar,
    private http: HttpClient) { 

    
  }

  clockForm = new FormGroup({
    date: new FormControl('', [Validators.required, dateBeforeOfTodayValidator()]),
    time: new FormControl('', [Validators.required, timePassedValidator(), timeFormatValidator]),
  });
  
  ngOnInit() {
  }

  createClockAlarm(){
    if (this.clockForm.valid) {
      let date = new Date(this.clockForm.value.date!);
      date.setDate(date.getDate() + 1);
      let dateString = date.toISOString().split('T')[0];
      let time = this.clockForm.get('time')?.value!;
      const queryParams = {
        date: dateString,
        time: time,
      };
      const environment = {
        production: false,
        apiGateway: 'http://localhost:5001', // Replace this with your API Gateway URL
      };
      const options: any = {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
        params: queryParams
      };
      this.http.post<any>(environment.apiGateway + "/clock-alarm", options).subscribe({
        next: (value: any) => {
          console.log(value);
        },
        error: (err) => {
          console.log(err);
        }
      });
      this.dialogRef.close();
    }
  }

  closeDialog(){
    this.dialogRef.close();
  }

}
