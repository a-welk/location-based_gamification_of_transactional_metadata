import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { HttpService } from './http.service';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private tokenKey = 'authToken';
  private loginStatus = new BehaviorSubject<boolean>(false);

  constructor(private HttpService: HttpService) {}

  login(email: string, password: string): Observable<any> {
    return this.HttpService.login(email, password).pipe(
      tap(response => {
        if (response.token) {
          this.setToken(response.token);
          this.loginStatus.next(true);
          console.log('Successful log in from AuthService:', response.token);
          console.log('Login Status:', this.loginStatus.value);
        }
      })
    );
  }

  isLoggedIn(): Observable<boolean> {
    return this.loginStatus.asObservable();
  }

  public getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  private setToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  private clearToken(): void {
    localStorage.removeItem(this.tokenKey);
  }
}
