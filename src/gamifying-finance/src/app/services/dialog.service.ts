import { Injectable } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { LoginComponent } from '../login/login.component';
import { SignupComponent } from '../signup/signup.component';

@Injectable({
  providedIn: 'root'
})
export class DialogService {
  private isDialogOpen = false;

  constructor(private dialog: MatDialog) { }

  openLoginDialog(): void {
    if (!this.isDialogOpen) {
      const dialogConfig = new MatDialogConfig();
      dialogConfig.width = '400px';
      dialogConfig.height = '400px';
      dialogConfig.position = { top: '-33%', left: '35%' };
      dialogConfig.panelClass = 'custom-dialog-container';
      dialogConfig.autoFocus = false;
      const dialogRef = this.dialog.open(LoginComponent, dialogConfig);

      this.isDialogOpen = true;

      dialogRef.afterClosed().subscribe(() => {
        this.isDialogOpen = false;
      });
    }
  }

  openSignupDialog(): void {
    if (!this.isDialogOpen) {
      const dialogConfig = new MatDialogConfig();
      dialogConfig.width = '400px';
      dialogConfig.height = '400px';
      dialogConfig.position = { top: '-33%', left: '35%' };
      dialogConfig.panelClass = 'custom-dialog-container';
      const dialogRef = this.dialog.open(SignupComponent, dialogConfig);

      this.isDialogOpen = true;

      dialogRef.afterClosed().subscribe(() => {
        this.isDialogOpen = false;
      });
    }
  }
}
