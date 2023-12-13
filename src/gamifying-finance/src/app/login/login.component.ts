import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DatabaseService } from '../database.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  email: string = '';
  password: string = '';

  constructor(private databaseService: DatabaseService) {}

  login() {
    
  }
  // login() {
  //   this.databaseService.login(this.email, this.password).subscribe({
  //     next: (response) => {
  //       // Handle successful login (navigate to another page, display a message, etc.)
  //       console.log('Login successful:', response);
  //     },
  //     error: (error) => {
  //       // Handle login error (display an error message, redirect, etc.)
  //       console.error('Login failed:', error);
  //     }
  //   });
  // }
}
