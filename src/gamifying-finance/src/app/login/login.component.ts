import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpService } from '../services/http.service';
import { FormsModule } from '@angular/forms';

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

  constructor(private HttpService: HttpService) {}

  login() {
    this.HttpService.login(this.email, this.password)
      .subscribe({
        next: response => console.log('Success!', response),
        error: error => console.error('Error!', error)
      });
  }
}
