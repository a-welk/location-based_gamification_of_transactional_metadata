import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpService } from '../services/http.service';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';

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
  subscription!: Subscription;
  subscriptionManager = [];

  constructor(private http: HttpService) {}

  ngOnInit(): void {
    // this.subscriptionManager.push(
    //   this.subscription.
    // )

  }

  ngOnDestroy(): void {


  }

  login() {
  //   this.http.getLogin(this.email, this.password).subscribe(
  //     (response) => {
  //       console.log('Login successful:', response);
  //     },
  //     (error) => {
  //       console.error('Login failed:', error);
  //     }
  //   );
  }
}
