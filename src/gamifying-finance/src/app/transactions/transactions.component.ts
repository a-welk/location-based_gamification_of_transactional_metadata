
import { OnInit } from '@angular/core';
import { TransactionService } from '../services/transactions.service';
import { Component } from '@angular/core';
import { NgForOf } from '@angular/common'; // Import NgFor directive

@Component({
  selector: 'app-transactions-component',
  templateUrl: './transactions.component.html',
  standalone: true,
  imports: [NgForOf], // Include NgForOf in the imports array
})

export class TransactionsComponent implements OnInit {
  transactions: any[] = [];

  constructor(private dataService: TransactionService) { }

  ngOnInit(): void {
    this.dataService.fetchData().subscribe((data: any[]) => { // Specify the type of the data parameter
      this.transactions = data.map((transaction: any) => { // Specify the type of the transaction parameter
        // Destructure to exclude unwanted properties and return the rest
        const { merchantUUID, UserUUID, UseChip, 'Is Fraud?': isFraud, ...rest } = transaction;
        console.log('rest', rest);
        return rest;
      });
    });
  }
}