import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { routes } from '../app.routes';
import { Router } from '@angular/router';

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './button.component.html',
  styleUrl: './button.component.css'
})
export class ButtonComponent implements OnInit{
  constructor(private router: Router) {}
  ngOnInit(){
      
  }
  goToPage(pagename: string) {
    this.router.navigate([pagename])
  }
  
}
