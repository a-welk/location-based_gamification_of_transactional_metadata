import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ExpensesComponent } from '../expenses/expenses.component';
import { StatusComponent } from '../status/status.component';
import { MapComponent } from '../map/map.component';
import { HistoryComponent } from '../history/history.component';
import { MonthlyExpensesComponent } from '../monthly-expenses/monthly-expenses.component';


@Component({
    selector: 'app-dashboard',
    standalone: true,
    templateUrl: './dashboard.component.html',
    styleUrl: './dashboard.component.css',
    imports: [CommonModule, StatusComponent, ExpensesComponent, MapComponent, HistoryComponent, MonthlyExpensesComponent]
})
export class DashboardComponent {

}
