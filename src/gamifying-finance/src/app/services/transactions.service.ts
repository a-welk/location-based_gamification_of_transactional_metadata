import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { catchError, Observable } from 'rxjs';
import { AuthService } from './auth.service';
import { Router } from '@angular/router'; // Import the Router

@Injectable({
  providedIn: 'root'
})
export class TransactionService {
  private apiUrl = 'http://127.0.0.1:5000/getTransactions';

  constructor(private http: HttpClient, private authService: AuthService, private router: Router) {} // Add router to the constructor

  fetchData(month: string, year: string): Observable<any> {
    const token = this.authService.getToken();
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    const params = new HttpParams().set('month', month).set('year', year);
  
    return this.http.get(this.apiUrl, { headers, params }).pipe(
      catchError((error) => {
        if (error.status === 401) {
          // Use the Router to navigate
          this.router.navigate(['/']); // Redirect user to '/'
        }
        throw error;
      })
    );
  }  
}
