import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgIconComponent, provideIcons } from '@ng-icons/core';
import { featherThumbsUp, featherThumbsDown, featherSettings } from '@ng-icons/feather-icons';

@Component({
  selector: 'app-status',
  standalone: true,
  imports: [CommonModule, NgIconComponent],
  viewProviders: [provideIcons({ featherThumbsUp, featherThumbsDown, featherSettings })],
  templateUrl: './status.component.html',
  styleUrl: './status.component.css'
})
export class StatusComponent {

  ngOnInit(): void {


  }

  checkBudget(): boolean {
    return true
  }
}
