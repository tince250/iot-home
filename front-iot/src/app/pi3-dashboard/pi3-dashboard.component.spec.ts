import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Pi3DashboardComponent } from './pi3-dashboard.component';

describe('Pi3DashboardComponent', () => {
  let component: Pi3DashboardComponent;
  let fixture: ComponentFixture<Pi3DashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ Pi3DashboardComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Pi3DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
