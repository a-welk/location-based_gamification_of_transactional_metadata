import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpService } from '../services/http.service';
import {CommonModule, NgIf} from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-leaderboard',
  standalone: true,
  templateUrl: './leaderboard.component.html',
  styleUrls: ['./leaderboard.component.css'],
  imports:[LeaderboardComponent, CommonModule, FormsModule]
})

export class LeaderboardComponent {
  zipcode: string = '';
  leaderboardData: any[] = [];
  selectedOption: string = 'showALL';
  inputted: boolean = false;
  token: any = '';
  loggedIn: any = false;

  constructor(private httpservice: HttpService, private authservice: AuthService) {}

  ngOnInIt(): void {
    this.leaderboard()
  }
  
  leaderboard() {
    if(this.authservice.isLoggedIn())
      this.token = this.authservice.getToken()
      this.httpservice.leaderboard(this.token)
      .subscribe({
        next: response => {
          console.log(response)
          this.inputted = true
          this.leaderboardData = response
        },
        error: error => console.error('Error!', error)
      });
  }

  executeLeaderboardFunction() {
    switch(this.selectedOption) {
      case 'showAll':
        this.token = this.authservice.getToken()
        this.httpservice.leaderboard(this.token)
        .subscribe({
          next: response => {
            console.log(response)
            this.leaderboardData = response
          },
          error: error => console.error('Error!', error)
        });
        break;
      case 'showMonth':
        this.token = this.authservice.getToken()
        this.httpservice.monthly_leaderboard(this.token)
        .subscribe({
          next: response => {
            console.log(response)
            this.leaderboardData = response
          },
          error: error => console.error('Error!', error)
        });
        break;
      }
    }
  }
