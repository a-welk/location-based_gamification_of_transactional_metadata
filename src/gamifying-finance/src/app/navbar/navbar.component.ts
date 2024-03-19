import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { DashboardComponent } from '../dashboard/dashboard.component';
import { LeaderboardComponent } from '../leaderboard/leaderboard.component';
import { LoginComponent } from '../login/login.component';
import { RouterLink } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Observable } from 'rxjs';
import { SignupComponent } from '../signup/signup.component';
import { DialogService } from '../services/dialog.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    CommonModule,
    DashboardComponent,
    LoginComponent,
    RouterLink,
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent implements OnInit {
  isLoggedIn$!: Observable<boolean>;
  loginDialogRef!: MatDialogRef<LoginComponent>;
  signupDialogRef!: MatDialogRef<SignupComponent>;

  constructor(public AuthService: AuthService, private dialogService: DialogService) {
  }

  ngOnInit() {
    this.isLoggedIn$ = this.AuthService.isLoggedIn();
  }

  openLoginDialog(): void {
    this.dialogService.openLoginDialog();
  }

  openSignupDialog(): void {
    this.dialogService.openSignupDialog();
  }
}
