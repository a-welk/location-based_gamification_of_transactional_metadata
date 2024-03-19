// backend.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import leaderboard from 'path'

@Injectable({
  providedIn: 'root',
})
export class LeaderboardService {
  private apiUrl = 'http://127.0.0.1:5000';j

  constructor(private http: HttpClient) {}

  leaderboard(zipcode: string): Observable<any> {
    const leaderboardUrl = this.apiUrl +'/leaderboard'; 
    return this.http.post(leaderboardUrl, { zipcode });
  }
}
