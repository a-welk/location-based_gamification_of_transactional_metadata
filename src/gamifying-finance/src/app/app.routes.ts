import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LeaderboardComponent } from './leaderboard/leaderboard.component';
import { LoginComponent } from './login/login.component';
import { NavbarComponent } from './navbar/navbar.component';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

export const routes: Routes = [
  {path: 'dashboard', component: DashboardComponent},
  {path: 'leaderboard', component: LeaderboardComponent},
  {path: 'login', component: LoginComponent},
  {path: 'navbar', component: NavbarComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
