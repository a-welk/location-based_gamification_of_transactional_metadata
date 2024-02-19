import { Injectable } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { LoginComponent } from '../login/login.component';
import { SignupComponent } from '../signup/signup.component';

@Injectable({
  providedIn: 'root'
})
export class DialogService {
  private dialogRefLogin: any;
  private dialogRefSignup: any;


  constructor(private dialog: MatDialog) { }

  openLoginDialog(): void {
    if (this.dialogRefSignup && this.dialogRefSignup.componentInstance instanceof SignupComponent) {
      this.dialogRefSignup.close();
      this.dialogRefSignup = null;
    }
    else if (!this.dialogRefLogin || !(this.dialogRefLogin.componentInstance instanceof LoginComponent)) {
      const dialogConfig = new MatDialogConfig();
      dialogConfig.width = '400px';
      dialogConfig.height = '400px';
      dialogConfig.position = { top: '-33%', left: '35%' };
      dialogConfig.autoFocus = false;
      this.dialogRefLogin = this.dialog.open(LoginComponent, dialogConfig);
    }
  }

  openSignupDialog(): void {
    if (this.dialogRefLogin && this.dialogRefLogin.componentInstance instanceof LoginComponent) {
      this.dialogRefLogin.close();
      this.dialogRefLogin = null;
    }
    else if (!this.dialogRefSignup || !(this.dialogRefSignup.componentInstance instanceof SignupComponent)) {
      const dialogConfig = new MatDialogConfig();
      dialogConfig.width = '400px';
      dialogConfig.height = '400px';
      dialogConfig.position = { top: '-33%', left: '35%' };
      dialogConfig.autoFocus = false;
      this.dialogRefSignup = this.dialog.open(SignupComponent, dialogConfig);
    }
  }
}
