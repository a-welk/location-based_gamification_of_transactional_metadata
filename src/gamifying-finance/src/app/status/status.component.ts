import { PaginatorModule } from 'primeng/paginator';
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgIconComponent, provideIcons } from '@ng-icons/core';
import { featherThumbsUp, featherThumbsDown, featherSettings } from '@ng-icons/feather-icons';
import { HttpService } from '../services/http.service';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-status',
  standalone: true,
  imports: [CommonModule, NgIconComponent],
  viewProviders: [provideIcons({ featherThumbsUp, featherThumbsDown, featherSettings })],
  templateUrl: './status.component.html',
  styleUrl: './status.component.css'
})
export class StatusComponent {

  constructor(private http: HttpService, private auth: AuthService) {

  }
  ngOnInit(): void {
    this.checkBudget();
  }

  checkBudget(): void {
    const token = this.auth.getToken();
    if (token) {
      this.http.get_monthly_transactions().subscribe({
        next: (response) => {
          console.log('Budget check:', response);
        },
        error: (error) => {
          console.error('Error fetching monthly transactions:', error);
        }
      });
    } else {
      console.error('User not logged in');
    }
  }
}
