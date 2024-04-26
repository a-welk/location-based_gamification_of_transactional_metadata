import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { BudgetService } from '../services/budget.service';
import { Budget } from '../models/budget.model';

// Define MonthMap and ReverseMonthMap types here
type MonthMap = {
  [key: number]: string;
};

type ReverseMonthMap = {
  [key: string]: string;
};

@Component({
  selector: 'app-categories-leaderboard',
  templateUrl: './categories-leaderboard.component.html',
  styleUrls: ['./categories-leaderboard.component.css'],
  standalone: true,
  imports: [FormsModule, CommonModule]
})
export class CategoriesLeaderboardComponent implements OnInit {

  public categoriesData: Budget | null = null;
  public selectedMonth: string = this.getCurrentMonth();
  public selectedYear: string = new Date().getFullYear().toString();
  public months: string[] = this.getMonthsArray();
  public years: string[] = this.getYearsArray();

  constructor(private dataService: BudgetService) { }

  ngOnInit(): void {
    this.getAverageData(this.reverseMonth(this.selectedMonth), this.selectedYear, 62621);
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

  getAverageData(month: string, year: string, zipcode: number): void {
    this.dataService.getAverageData(month, year, zipcode).subscribe(
      data => this.categoriesData = data,
      error => console.error('There was an error!', error)
    );
  }

  onMonthChange(newMonth: string): void {
    this.selectedMonth = newMonth;
    this.getAverageData(this.reverseMonth(this.selectedMonth), this.selectedYear, 62621);
  }
  
  onYearChange(newYear: string): void {
    this.selectedYear = newYear;
    this.getAverageData(this.selectedMonth, this.selectedYear, 62621);
  }
}
