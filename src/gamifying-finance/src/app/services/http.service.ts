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

  leaderboard(token: string): Observable<any> {
    const leaderboardUrl = this.apiUrl +'/leaderboard';
    return this.http.post(leaderboardUrl,  {token});
  }

  monthly_leaderboard(token: string, selectedMonth: any, selectedYear: any): Observable<any> {
    const leaderboardUrl = this.apiUrl +'/monthly_leaderboard';
    return this.http.post(leaderboardUrl,  {token, selectedMonth, selectedYear});
  }

  get_monthly_transactions() {
    const url = this.apiUrl +'/get_monthly_transactions';
    return this.http.get(url);
  }

  update_budget_option(budgetChoice: any) {
    const url = this.apiUrl +'/update_budget_option';
    return this.http.post(url, { budgetChoice })
  }


}
