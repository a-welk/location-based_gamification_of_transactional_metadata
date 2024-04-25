
import { OnInit } from '@angular/core';
import { TransactionService } from '../services/transactions.service';
import { Component } from '@angular/core';
import { NgForOf } from '@angular/common'; // Import NgFor directive
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-transactions-component',
  templateUrl: './transactions.component.html',
  styleUrls: ['./transactions.component.css'],
  standalone: true,
  imports: [NgForOf, FormsModule], // Include NgForOf in the imports array
})

export class TransactionsComponent implements OnInit {
  transactions: any[] = [];
  selectedMonth: string = "";
  selectedYear: string = "";
  months: string[] = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'];
  years: string[] = ['2021', '2022', '2023', '2024', '2025'];

  constructor(private transactionService: TransactionService) { }

  ngOnInit(): void {
    // Initialize the years dynamically or statically as needed
    this.years = this.generateYears();

    // Optionally, auto-select the current month and year
    const currentDate = new Date();
    this.selectedMonth = this.months[currentDate.getMonth()];
    this.selectedYear = currentDate.getFullYear().toString();

    // Fetch data based on the selected month and year
    this.fetchData();
  }

  fetchData() {
    this.transactionService.fetchData(this.selectedMonth, this.selectedYear).subscribe((data: any[]) => {
      console.log('Data:', data);
      this.transactions = data.map((transaction: any) => {
        const { merchantUUID, UserUUID, UseChip, 'Is Fraud?': isFraud, ...rest } = transaction;
        console.log('Transaction data:', rest);
        return rest;
      });
    });
  }

  onMonthChange(newMonth: string) {
    this.selectedMonth = newMonth;
    this.fetchData();
  }

  onYearChange(newYear: string) {
    this.selectedYear = newYear;
    this.fetchData();
  }

  // Helper function to generate year range for selection
  private generateYears(): string[] {
    const currentYear = new Date().getFullYear();
    const startYear = currentYear - 10; // for the past 10 years
    const years = [];
    for (let year = startYear; year <= currentYear; year++) {
      years.push(year.toString());
    }
    return years;
  }
}