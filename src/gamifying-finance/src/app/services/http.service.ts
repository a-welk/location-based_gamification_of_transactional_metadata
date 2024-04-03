import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  private apiUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) { }

  signup(email: String, password: String) {
    const signupUrl = this.apiUrl + '/signup';
    return this.http.post(signupUrl, { email, password });
  }

  login(email: String, password: String): Observable<any> {
    const loginUrl = this.apiUrl + '/login';
    return this.http.post(loginUrl, { email, password });
  }

  getUserName(): Observable<any> {
    const name = this.apiUrl + '/name';
    return this.http.get(name);
  }

  leaderboard(token: string): Observable<any> {
    const leaderboardUrl = this.apiUrl +'/leaderboard'; 
    return this.http.post(leaderboardUrl,  {token});
  }

  monthly_leaderboard(token: string, selectedMonth: any, selectedYear: any): Observable<any> {
    const leaderboardUrl = this.apiUrl +'/monthly_leaderboard'; 
    return this.http.post(leaderboardUrl,  {token, selectedMonth, selectedYear});
  }
}
