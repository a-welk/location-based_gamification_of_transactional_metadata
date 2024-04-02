import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
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

  transactions(page: number = 0, pageSize: number = 10): Observable<any> {
    const transactionsUrl = `${this.apiUrl}/transactions`;
    const authToken = localStorage.getItem('authToken');
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${authToken}`
    });
    let params = new HttpParams()
    .append('page', page.toString())
    .append('pageSize', pageSize.toString());

    return this.http.get(transactionsUrl, { headers: headers, params: params });
  }

  leaderboard(token: string): Observable<any> {
    const leaderboardUrl = this.apiUrl +'/leaderboard'; 
    return this.http.post(leaderboardUrl,  {token});
  }

  monthly_leaderboard(token: string): Observable<any> {
    const leaderboardUrl = this.apiUrl +'/monthly_leaderboard'; 
    return this.http.post(leaderboardUrl,  {token});
  }
}
