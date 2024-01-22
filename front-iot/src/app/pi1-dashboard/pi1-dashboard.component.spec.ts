import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Pi1DashboardComponent } from './pi1-dashboard.component';

describe('Pi1DashboardComponent', () => {
  let component: Pi1DashboardComponent;
  let fixture: ComponentFixture<Pi1DashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ Pi1DashboardComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Pi1DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
