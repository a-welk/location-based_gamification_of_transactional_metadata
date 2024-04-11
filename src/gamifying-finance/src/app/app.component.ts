import { Component, Inject, NgModule, PLATFORM_ID } from '@angular/core';
import {NgIf, isPlatformBrowser} from '@angular/common';
import { FormsModule } from '@angular/forms';

import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { NavbarComponent } from './navbar/navbar.component';
import { LoginComponent } from './login/login.component';
import { LeaderboardComponent } from './leaderboard/leaderboard.component';
import { BehaviorSubject } from 'rxjs';
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

  isBrowser = new BehaviorSubject<boolean>(false);

  constructor(@Inject(PLATFORM_ID) private platformId: any) {
    this.isBrowser.next(isPlatformBrowser(this.platformId));
  }
}
