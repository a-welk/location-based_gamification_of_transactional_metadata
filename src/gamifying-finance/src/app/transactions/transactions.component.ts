import { Component, OnInit } from '@angular/core';
import { TransactionService } from '../services/transactions.service';
import { NgForOf } from '@angular/common';
import { FormsModule } from '@angular/forms';

type MonthMap = {
  [key: number]: string;
};

type ReverseMonthMap = {
  [key: string]: string;
};

@Component({
  selector: 'app-transactions-component',
  templateUrl: './transactions.component.html',
  styleUrls: ['./transactions.component.css'],
  standalone: true,
  imports: [NgForOf, FormsModule],
})



export class TransactionsComponent implements OnInit {
  transactions: any[] = [];
  filteredTransactions: any[] = [];
  searchTerm: string = '';
  public selectedMonth: string = this.getCurrentMonth();
  public selectedYear: string = new Date().getFullYear().toString();
  public months: string[] = this.getMonthsArray();
  public years: string[] = this.getYearsArray();

  constructor(private transactionService: TransactionService) {}

  ngOnInit(): void {
    this.fetchData(this.reverseMonth(this.selectedMonth), this.selectedYear);
  }


  fetchData(month: string, year: string,) {
    this.transactionService.fetchData(month, year).subscribe((data: any[]) => {
      this.transactions = data;
      this.filteredTransactions = data;
      this.filterTransactions(); // Apply initial filter (if any)
    });
  }

  getCurrentMonth(): string {
    const currentMonthIndex: number = new Date().getMonth() + 1;
    const month_json: MonthMap = {
      1: 'January', 2: 'February', 3: 'March', 4: 'April',
      5: 'May', 6: 'June', 7: 'July', 8: 'August',
      9: 'September', 10: 'October', 11: 'November', 12: 'December'
    };
    return month_json[currentMonthIndex];
  }
  reverseMonth(month : string): string {
    const reverse_month_json: ReverseMonthMap = { "January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06", "July": "07", "August": "08", "September": "09", "October": "10", "November": "11", "December": "12" };
    return reverse_month_json[month];
  }

  getMonthsArray(): string[] {
    return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  }
  
  getYearsArray(): string[] {
    let currentYear = new Date().getFullYear();
    return Array.from({ length: 5 }, (_, i) => (currentYear - i).toString());
  }

  onMonthChange(newMonth: string): void {
    this.selectedMonth = newMonth; // Maintain the month name for display purposes
    const monthValue = this.reverseMonth(newMonth); // Get the numeric string representation
    this.fetchData(monthValue, this.selectedYear); // Fetch data using the numeric value
  }

  onYearChange(newYear: string): void {
    this.selectedYear = newYear;
    this.fetchData(this.selectedMonth, this.selectedYear);
  }

  filterTransactions(): void {
    if (!this.searchTerm) {
      this.filteredTransactions = this.transactions;
    } else {
      this.filteredTransactions = this.transactions.filter(transaction =>
        Object.values(transaction).some(val =>
          (val as string).toString().toLowerCase().includes(this.searchTerm.toLowerCase())
        )
      );
    }
  }

}
