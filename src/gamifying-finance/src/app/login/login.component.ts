import { AuthService } from './../services/auth.service';
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpService } from '../services/http.service';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ],
  providers: [HttpService, AuthService],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  email: string = '';
  password: string = '';

  constructor(private HttpService: HttpService, private AuthService: AuthService, private Router: Router) {}

  login() {
    this.AuthService.login(this.email, this.password)
      .subscribe({
        next: response => {
          if (response.token) {
            console.log('Successfully logged in! Token received:', response.token);
            this.Router.navigate(['/dashboard'])
          }

        },
        error: error => console.error('Error!', error)
      });
  }
}
