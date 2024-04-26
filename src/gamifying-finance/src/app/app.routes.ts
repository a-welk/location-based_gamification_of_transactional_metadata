import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LeaderboardComponent } from './leaderboard/leaderboard.component';
import { LoginComponent } from './login/login.component';
import { NavbarComponent } from './navbar/navbar.component';
import { HomeComponent } from './home/home.component';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { SignupComponent } from './signup/signup.component';
import { TransactionsComponent } from './transactions/transactions.component';
import { Onboarding1Component } from './onboarding1/onboarding1.component';
import { Onboarding2Component } from './onboarding2/onboarding2.component';
import { MapComponent } from './map/map.component';
import { CategoriesLeaderboardComponent } from './categories-leaderboard/categories-leaderboard.component';
import { ExpensesComponent } from './expenses/expenses.component';
import { HistoryComponent } from './history/history.component';
import { MonthlyExpensesComponent } from './monthly-expenses/monthly-expenses.component';



export const routes: Routes = [
  {path: 'dashboard', component: DashboardComponent},
  {path: 'leaderboard', component: LeaderboardComponent},
  {path: 'login', component: LoginComponent},
  {path: 'signup', component: SignupComponent},
  {path: 'navbar', component: NavbarComponent},
  {path: 'home', component: HomeComponent},
  {path: 'transactions', component: TransactionsComponent},
  {path: 'onboarding', component: Onboarding1Component },
  {path: 'onboarding2', component: Onboarding2Component },
  {path: 'map', component: MapComponent },
  {path: 'categories', component: CategoriesLeaderboardComponent},
  {path: 'history', component: HistoryComponent},
  {path: 'expenses', component: ExpensesComponent},
  {path: 'monthly-expenses', component: MonthlyExpensesComponent},
  {path: '**', component: HomeComponent, pathMatch: 'full'},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
