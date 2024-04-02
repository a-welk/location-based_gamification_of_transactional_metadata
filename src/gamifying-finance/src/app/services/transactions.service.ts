import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, Observable } from 'rxjs';
import { AuthService } from './auth.service'; // Import the AuthService class

@Injectable({
  providedIn: 'root'
})
export class TransactionService {

  private apiUrl = 'http://127.0.0.1:5000/getTransactions';

  constructor(private http: HttpClient, private authService: AuthService) { } // Add authService parameter

  fetchData(): Observable<any> {
    const token = this.authService.getToken();
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    return this.http.get(this.apiUrl, { headers }).pipe(
      catchError((error) => {
        if (error.status === 401) {
          // Redirect user to '/'
          window.location.href = '/';
        }
        throw error;
      })
    );
  }
}
