import { Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LeaderboardComponent } from './leaderboard/leaderboard.component';

export const routes: Routes = [
  {path: 'dashboard', component: DashboardComponent},
  {path: 'leaderboard', component: LeaderboardComponent}
];
