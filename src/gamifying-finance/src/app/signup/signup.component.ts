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

  constructor(private HttpService: HttpService, private dialogRef: MatDialogRef<SignupComponent>, private Router: Router) {}

  checkPasswordMatch() {
    this.matching = this.password === this.confirmPassword;
  }

  signup() {
    this.checkPasswordMatch();
    if (this.matching == false) {
      console.error('Passwords do not match');
    } else {
      this.HttpService.signup(this.email, this.password)
        .subscribe({
          next: response => {
            console.log('Success!', response)
            this.closeDialog();
            this.Router.navigate(['/dashboard'])
          },
          error: error => console.error('Error!', error)
        });
    }
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
