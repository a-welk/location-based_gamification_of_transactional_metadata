import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from '../dashboard/dashboard.component';
import { LeaderboardComponent } from '../leaderboard/leaderboard.component';
import { LoginComponent } from '../login/login.component';
import { RouterLink } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    CommonModule,
    DashboardComponent,
    LeaderboardComponent,
    LoginComponent,
    RouterLink,
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent implements OnInit {
  isLoggedIn$: Observable<boolean>;

  constructor(public AuthService: AuthService) {
    this.isLoggedIn$ = this.AuthService.isLoggedIn();
  }

  ngOnInit() {

  }

  logout() {
    this.AuthService.logout();
  }
}
