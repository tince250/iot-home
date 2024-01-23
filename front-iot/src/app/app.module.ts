import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from '../infrastructure/app-routing.module';
import { AppComponent } from './app.component';
import { MaterialModule } from '../infrastructure/material.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { MAT_FORM_FIELD_DEFAULT_OPTIONS, MatFormFieldModule } from '@angular/material/form-field';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { NavbarComponent } from './navbar/navbar.component';
import { Pi1DashboardComponent } from './pi1-dashboard/pi1-dashboard.component';
import { Pi2DashboardComponent } from './pi2-dashboard/pi2-dashboard.component';
import { Pi3DashboardComponent } from './pi3-dashboard/pi3-dashboard.component';
import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';
import { CreateClockAlarmDialogComponent } from './create-clock-alarm-dialog/create-clock-alarm-dialog.component';
import {NgxMaterialTimepickerModule} from 'ngx-material-timepicker';

const config: SocketIoConfig = { url: 'localhost:5001', options: {} };

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    Pi1DashboardComponent,
    Pi2DashboardComponent,
    Pi3DashboardComponent,
    CreateClockAlarmDialogComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    MaterialModule,
    FormsModule,
    HttpClientModule,
    MatSnackBarModule,
    CommonModule,
    MatFormFieldModule,
    NgxMaterialTimepickerModule,
    SocketIoModule.forRoot(config)
  ],
  providers: [
    { provide: MAT_DIALOG_DATA, useValue: {} },
    {
      provide: MatDialogRef,
      useValue: {}
    },
    { provide: MAT_FORM_FIELD_DEFAULT_OPTIONS, useValue: { appearance: 'outline', hideRequiredMarker: 'true' }}
    ,],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  bootstrap: [AppComponent]
})
export class AppModule { }
