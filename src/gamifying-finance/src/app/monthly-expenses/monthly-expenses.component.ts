import { Component, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { AccumulationChart } from '@syncfusion/ej2-angular-charts';
import { Router } from '@angular/router';

@Component({
  selector: 'app-monthly-expenses',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './monthly-expenses.component.html',
  styleUrl: './monthly-expenses.component.css'
})
export class MonthlyExpensesComponent {
  chart: AccumulationChart | undefined

  constructor(private router: Router, @Inject(PLATFORM_ID) private platformId: object) {}


  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.initializeCharts();
    }
  }

  initializeCharts() {
    let chart1 : AccumulationChart = new AccumulationChart({
      series: [
          {
              dataSource: [{ x: 'Needs', y: 35 },
              { x: 'Wants', y: 50 },
              { x: 'Savings', y: 15 } ],
              type:'Pie',
              xName: 'x',
              yName: 'y',
              dataLabel: {
                visible: true
            }
          }
      ]
    }, '#chart');
  }
}
