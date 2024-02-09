import { Component, OnInit } from '@angular/core';
import { TransactionService } from '../services/transactions.service'; // Adjust the path as necessary

@Component({
  selector: 'app-transactions',
  templateUrl: './transactions.component.html',
  styleUrls: ['./transactions.component.css']
})
export class TransactionsComponent implements OnInit {
  transactions: any = [];

  constructor(private transactionService: TransactionService) { }

  ngOnInit(): void {
    this.transactionService.getTransactions().subscribe(data => {
      this.transactions = data['1']; // Adjust according to your data structure
    });
  }
}
