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

  async getLogin(email: string, pass: string): Promise<any> {
    this.inputEmail = email;
    this.inputPass = pass;
    const data = await fetch(this.apiUrl);

    const response = await this.http.post<any>(`${this.apiUrl}/login`, {
      email: this.inputEmail,
      password: this.inputPass
    });

    return response;
  }
}
