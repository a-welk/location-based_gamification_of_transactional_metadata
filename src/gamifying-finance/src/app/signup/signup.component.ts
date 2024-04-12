import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpService } from '../services/http.service';
import { AuthService } from '../services/auth.service';
import { MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})
export class SignupComponent {
  email: string = '';
  password: string = '';
  confirmPassword: string = '';
  matching: boolean = true;
  isValidEmail: boolean = true;
  isPasswordEmpty: boolean = false;

  constructor(private HttpService: HttpService, private dialogRef: MatDialogRef<SignupComponent>, private Router: Router) {}

  checkPasswordMatch() {
    this.matching = this.password === this.confirmPassword;
  }

    validateEmail() {
      const regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      this.isValidEmail = regex.test(this.email);
    }

    checkPasswordEmpty() {
      this.isPasswordEmpty = !this.password;
    }

  signup() {
    this.checkPasswordMatch();
    if (this.matching == false) {
      console.error('Passwords do not match');

    } else if (!this.validateEmail) {
      this.isValidEmail = false;
    } else if (this.isPasswordEmpty) {
      this.isPasswordEmpty = true;
    } else {
      this.HttpService.signup(this.email, this.password)
        .subscribe({
          next: response => {
            console.log('Success!', response)
            this.closeDialog();
            this.Router.navigate(['/home'])
          },
          error: error => console.error('Error!', error)
        });
    }
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
