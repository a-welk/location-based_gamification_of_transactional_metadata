import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { LeaderboardService } from '../services/leaderboard.service';
import { HttpService } from '../services/http.service';

@Component({
  selector: 'app-leaderboard',
  standalone: true,
  templateUrl: './leaderboard.component.html',
  styleUrls: ['./leaderboard.component.css'],
  imports:[LeaderboardComponent]
})
export class LeaderboardComponent {
  zipcode: string = '';
  leaderboardData: any[] = [];

  constructor(private leaderboardService: LeaderboardService) {}

  leaderboard() {
    // Replace 'your_backend_api_url' with the actual URL of your backend API
    this.leaderboardService.leaderboard(this.zipcode)
      .subscribe({
        next: response => {
          if(response.status == 200) {
            console.log(response.body)
          }
        },
      });

  }
}
