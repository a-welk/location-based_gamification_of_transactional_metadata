import { Component, NgModule } from '@angular/core';
import {NgIf} from '@angular/common';
import { FormsModule } from '@angular/forms';

import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { NavbarComponent } from './navbar/navbar.component';
import { LoginComponent } from './login/login.component';
import { LeaderboardComponent } from './leaderboard/leaderboard.component';
@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.component.html',
  imports: [
    NavbarComponent,
    LoginComponent,
    RouterModule,
    CommonModule,
    FormsModule,
    LeaderboardComponent
  ],
  styleUrls: ['./app.component.css']
}) 
export class AppComponent {
  title = 'gamifying-finance';
}
