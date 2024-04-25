import { Component, OnInit, NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { BudgetService } from '../services/budget.service';
import { Budget } from '../models/budget.model';

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
    this.getAverageData(this.selectedMonth, this.selectedYear, 62621);
  }

  getCurrentMonth(): string {
    // JavaScript getMonth() is 0-indexed; adding 1 to get 1-indexed month
    let currentMonth = new Date().getMonth() + 1;
    return currentMonth < 10 ? `0${currentMonth}` : `${currentMonth}`;
  }

  getMonthsArray(): string[] {
    return Array.from({ length: 12 }, (_, i) => (i + 1).toString().padStart(2, '0'));
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
    this.getAverageData(this.selectedMonth, this.selectedYear, 62621);
  }
  
  onYearChange(newYear: string): void {
    this.selectedYear = newYear;
    this.getAverageData(this.selectedMonth, this.selectedYear, 62621);
  }
}
