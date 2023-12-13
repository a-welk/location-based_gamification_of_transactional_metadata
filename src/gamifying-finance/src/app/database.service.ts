import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {
  // private apiUrl = 'http://127.0.0.1:5000';


  // constructor(private http: HttpClient) { }

  // login(email: string, password: string): Observable<any> {
  //   const body = { email, password };

  //   return this.http.post<any>(`${this.apiUrl}/login`, body);
  // }
}
