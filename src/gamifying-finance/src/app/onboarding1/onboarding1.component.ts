import { Component, Inject, OnInit, PLATFORM_ID } from '@angular/core';
import { Series, AccumulationChart, PieSeries } from '@syncfusion/ej2-charts';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-onboarding1',
  templateUrl: './onboarding1.component.html',
  styleUrls: ['./onboarding1.component.css'],
  standalone: true
})
export class Onboarding1Component implements OnInit {
  chart1: AccumulationChart | undefined
  chart2: AccumulationChart | undefined
  chart3: AccumulationChart | undefined

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
              dataSource: [{x: 'Needs', y: 70 },
              { x: 'Savings & Debt Repayment', y: 20 },
              { x: 'Donation or Additional Savings', y: 10 }],
              type:'Pie',
              xName: 'x',
              yName: 'y',
              dataLabel: {
                visible: true,
                name: 'text',
                template:  "<div id='templateWrap' style='background-color:#bd18f9;border-radius: 3px; float: right;padding: 2px;line-height: 20px;text-align: center;'>"+ "<img src='https://ej2.syncfusion.com/demos/src/chart/images/sunny.png' />" + "<div style='color:white; font-family:Roboto; font-style: medium; fontp-size:14px;float: right;padding: 2px;line-height: 20px;text-align: center;padding-right:6px'><span>${point.y}</span></div></div>"
            }
          }
      ]
  }, '#chart1');
  let chart2 : AccumulationChart = new AccumulationChart({
    series: [
        {
            dataSource: [{ x: 'Needs', y: 50 },
            { x: 'Wants', y: 30 },
            { x: 'Savings', y: 20 } ],
            type:'Pie',
            xName: 'x',
            yName: 'y',
            dataLabel: {
              visible: true
          }
        }
    ]
  }, '#chart2');
  let chart3 : AccumulationChart = new AccumulationChart({
    series: [
        {
            dataSource: [{ x: 'Taxes', y: 40 },
            { x: 'Savings', y: 40 },
            { x: 'Living Expenses', y: 20 }  ],
            type:'Pie',
            xName: 'x',
            yName: 'y',
            dataLabel: {
              visible: true
          }
        }
    ]
  }, '#chart3');
  }

  renderChart(title: string, data: PieSeries[], elementId: string) {
    let chart: AccumulationChart = new AccumulationChart({
      series: [{
        dataSource: data,
        xName: 'x',
        yName: 'y'
      }],
      title: title,
      legendSettings: { visible: true }
    });
    chart.appendTo('#' + elementId);
  }

  nextPage(){
    this.router.navigate(["/onboarding2"])
  }
}
