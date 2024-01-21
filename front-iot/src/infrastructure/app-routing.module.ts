import { Pi1DashboardComponent } from './../app/pi1-dashboard/pi1-dashboard.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {path: 'pi1', component: Pi1DashboardComponent},
  {path: 'pi2', component: Pi1DashboardComponent},
  {path: 'pi3', component: Pi1DashboardComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { 

}
