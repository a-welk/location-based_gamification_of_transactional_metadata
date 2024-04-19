import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MonthlyExpensesComponent } from './monthly-expenses.component';

describe('MonthlyExpensesComponent', () => {
  let component: MonthlyExpensesComponent;
  let fixture: ComponentFixture<MonthlyExpensesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MonthlyExpensesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MonthlyExpensesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
