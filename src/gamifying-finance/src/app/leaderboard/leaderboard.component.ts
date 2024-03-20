import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpService } from '../services/http.service';
import {CommonModule, NgIf} from '@angular/common';
import { FormsModule } from '@angular/forms';

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

  constructor(private httpservice: HttpService) {}

  leaderboard() {
    this.httpservice.leaderboard(this.zipcode)
      .subscribe({
        next: response => {
          if(response.status == 200) {
            console.log(response.body);
            return response.body;
          }
        },
        error: error => console.error('Error!', error)
      });
      
  }
}
