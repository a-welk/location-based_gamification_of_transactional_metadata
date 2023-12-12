import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from '../dashboard/dashboard.component';
import { LeaderboardComponent } from '../leaderboard/leaderboard.component';
import { LoginComponent } from '../login/login.component';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    CommonModule,
    DashboardComponent,
    LeaderboardComponent,
    LoginComponent,
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent implements OnInit {
  isCollapsed : boolean = true;

  toggleCollapse() {
    this.isCollapsed = !this.isCollapsed;
  }

  ngOnInit() {

  }
}
