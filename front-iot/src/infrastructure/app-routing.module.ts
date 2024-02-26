import { Pi1DashboardComponent } from './../app/pi1-dashboard/pi1-dashboard.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AlarmsComponent } from 'src/app/alarms/alarms.component';
import { Pi2DashboardComponent } from 'src/app/pi2-dashboard/pi2-dashboard.component';
import { Pi3DashboardComponent } from 'src/app/pi3-dashboard/pi3-dashboard.component';

const routes: Routes = [
  {path: '*', component: Pi1DashboardComponent},
  {path: 'pi1', component: Pi1DashboardComponent},
  {path: 'pi2', component: Pi2DashboardComponent},
  {path: 'pi3', component: Pi3DashboardComponent},
  {path: 'alarms', component: AlarmsComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { 

}
