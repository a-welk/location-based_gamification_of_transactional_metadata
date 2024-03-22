import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Transaction } from '../interface/transaction';

@Component({
  selector: 'app-displaytransactions',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './displaytransactions.component.html',
  styleUrl: './displaytransactions.component.css'
})
export class DisplaytransactionsComponent {
  @Input() transactions!: Transaction[];
}
