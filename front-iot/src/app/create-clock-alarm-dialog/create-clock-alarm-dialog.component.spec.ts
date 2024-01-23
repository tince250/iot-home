import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateClockAlarmDialogComponent } from './create-clock-alarm-dialog.component';

describe('CreateClockAlarmDialogComponent', () => {
  let component: CreateClockAlarmDialogComponent;
  let fixture: ComponentFixture<CreateClockAlarmDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CreateClockAlarmDialogComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateClockAlarmDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
