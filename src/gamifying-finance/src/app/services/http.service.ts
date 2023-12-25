import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  private apiUrl = 'http://127.0.0.1:5000';
  private inputEmail: String = '';
  private inputPass: String = '';

  constructor(private http: HttpClient) { }

  login(email: string, password: string): Observable<any> {
    const loginUrl = this.apiUrl + '/login';
    return this.http.post(loginUrl, { email, password });
  }
}
