import { Component, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { Router } from '@angular/router';
import { Chart, LineSeries } from '@syncfusion/ej2-angular-charts';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './history.component.html',
  styleUrl: './history.component.css'
})
export class HistoryComponent {
  chart: Chart | undefined
  constructor(private router: Router, @Inject(PLATFORM_ID) private platformId: object) {}


  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.initializeCharts();
    }
  }

  initializeCharts() {
  let chart = new Chart({
    series:[{
        dataSource: [
          { x: 'May', y: 1982 }, { x: 'Jun', y: 2321 },{ x: 'Jul', y: 2011 }, { x: 'Aug', y: 2555 },
          { x: 'Sep', y: 2341 }, { x: 'Oct', y: 2312 }, { x: 'Nov', y: 1945 }, { x: 'Dec', y: 2341 },
          { x: 'Jan', y: 2700 }, { x: 'Feb', y: 2503}, { x: 'Mar', y: 2459}, { x: 'Apr', y: 2410}
        ],
        xName: 'y', yName: 'x',
        fill: 'green',
        opacity: '0',
        type: 'line'
        
    }],
  }, '#element');
  }
}
