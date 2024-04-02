import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DataViewModule } from 'primeng/dataview';
import { PaginatorModule } from 'primeng/paginator';
import { HttpService } from '../services/http.service';

@Component({
  selector: 'app-transactions',
  standalone: true,
  imports: [CommonModule, DataViewModule, PaginatorModule],
  templateUrl: './transactions.component.html',
  styleUrl: './transactions.component.css'
})
export class TransactionsComponent {
  transactions: any[] = [];
  totalRecords: number = 0;
  rows: number = 10;

  constructor(private httpService: HttpService) {
  }

  ngOnInit() {
    this.loadTransactions();
  }

  loadTransactions(page: number = 0) {
    this.httpService.transactions(page, this.rows).subscribe({
      next: (data) => {
        this.transactions = data.transactions;
        this.totalRecords = data.totalRecords;
      },
      error: (error) => {
        console.error('Failed to load transactions:', error);
      }
    });
  }

  paginate(event: any) {
    this.loadTransactions(event.page);
  }
}

