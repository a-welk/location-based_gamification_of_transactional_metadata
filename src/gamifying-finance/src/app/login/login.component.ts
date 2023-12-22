import { Component, Injector, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpService } from '../services/http.service';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHandler } from '@angular/common/http';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ],
  providers: [HttpService],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  email: string = '';
  password: string = '';
  private promise: Promise<void> | undefined;

  constructor(private HttpService: HttpService) {}

  login(): void {
    this.promise = this.HttpService.getLogin(this.email, this.password)
      .then(
        response => {
          console.log(response);
        }
      )
      .catch(
        error => {
          console.error(error);
        }
      );
  }
}
