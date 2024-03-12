// src/app/transactions/transactions.component.ts
import { Component, OnInit } from '@angular/core';
import { TransactionService } from '../services/transactions.service';
import { CommonModule } from '@angular/common'; // Import CommonModule

@Component({
  selector: 'app-transactions',
  templateUrl: './transactions.component.html',
  styleUrls: ['./transactions.component.css'],
  providers: [TransactionService] // Add DataService to the providers array
})
export class TransactionsComponent implements OnInit {
  transactions: any[] = [];

  constructor(private dataService: TransactionService) { }

  ngOnInit(): void {
    this.dataService.fetchData().subscribe((data: any[]) => { // Specify the type of the data parameter
      this.transactions = data.map((transaction: any) => { // Specify the type of the transaction parameter
        // Destructure to exclude unwanted properties and return the rest
        const { merchantUUID, UserUUID, UseChip, 'Is Fraud?': isFraud, ...rest } = transaction;
        return rest;
      });
    });
  }
}