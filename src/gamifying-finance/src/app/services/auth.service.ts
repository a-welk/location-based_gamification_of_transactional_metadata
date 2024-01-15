import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { HttpService } from './http.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private loggedIn = new BehaviorSubject<boolean>(false);

  constructor(private HttpService: HttpService) {}

  login(email: string, password: string): Observable<any> {
    return this.HttpService.login(email, password).pipe(
      tap(response => {
        // Handle login success, store the token, etc...
        this.loggedIn.next(true);
        console.log(this.loggedIn);
      })
    );
  }

  isLoggedIn() {
    return this.loggedIn.asObservable();
  }

  logout() {
    this.loggedIn.next(false);
    console.log('Logged out');
  }
}
