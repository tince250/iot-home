import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Pi2DashboardComponent } from './pi2-dashboard.component';

describe('Pi2DashboardComponent', () => {
  let component: Pi2DashboardComponent;
  let fixture: ComponentFixture<Pi2DashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ Pi2DashboardComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Pi2DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
