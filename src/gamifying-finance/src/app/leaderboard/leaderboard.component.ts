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
  selectedYear: any = "";
  selectedMonth: any = "";

  months = [
    { label: 'January', value: 1 },
    { label: 'February', value: 2 },
    { label: 'March', value: 3 },
    { label: 'April', value: 4 },
    { label: 'May', value: 5 },
    { label: 'June', value: 6 },
    { label: 'July', value: 7 },
    { label: 'August', value: 8 },
    { label: 'September', value: 9 },
    { label: 'October', value: 10 },
    { label: 'November', value: 11 },
    { label: 'December', value: 12 }
  ];

  years = Array.from({ length: 2024 - 2000 + 1 }, (_, index) => 2000 + index);

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
        this.httpservice.monthly_leaderboard(this.token, this.selectedMonth, this.selectedYear)
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

  onLeaderboardOptionChange() {
    // Reset input values when the option changes
    if (this.selectedOption === 'showAll') {
      this.executeLeaderboardFunction();
    }
    this.selectedMonth = null;
    this.selectedYear = null;
  }
  
    
  }
