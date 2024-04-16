import { Component, Inject, NgModule, PLATFORM_ID, Renderer2 } from '@angular/core';
import {DOCUMENT, NgIf, isPlatformBrowser} from '@angular/common';
import { FormsModule } from '@angular/forms';

import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { NavbarComponent } from './navbar/navbar.component';
import { LoginComponent } from './login/login.component';
import { LeaderboardComponent } from './leaderboard/leaderboard.component';
import { Onboarding1Component } from './onboarding1/onboarding1.component';
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
    LeaderboardComponent,
    Onboarding1Component
  ],
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'gamifying-finance';

  isBrowser = new BehaviorSubject<boolean>(false);

  constructor(@Inject(PLATFORM_ID) private platformId: any, private renderer2: Renderer2,
  @Inject(DOCUMENT) private document: Document) {
    this.isBrowser.next(isPlatformBrowser(this.platformId));
  }


  ngOnInit() {
    const s = this.renderer2.createElement('script');
    s.type = 'text/javascript';
    s.src = `https://maps.googleapis.com/maps/api/js?key=INSERT_KEY_HERE`;
    s.defer = true;
    s.async = true;
    this.renderer2.appendChild(this.document.head, s);
  }
}

