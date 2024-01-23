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
    private snackBar: MatSnackBar) { 

    
  }

  clockForm = new FormGroup({
    date: new FormControl('', [Validators.required, dateBeforeOfTodayValidator()]),
    time: new FormControl('', [Validators.required, timePassedValidator(), timeFormatValidator]),
  });
  
  ngOnInit() {
  }

  createClockAlarm(){
    if (this.clockForm.valid) {
      console.log(new Date(this.clockForm.value.date!).toISOString().split('T')[0]);
      this.dialogRef.close();
    }
  }

  closeDialog(){
    this.dialogRef.close();
  }

}
