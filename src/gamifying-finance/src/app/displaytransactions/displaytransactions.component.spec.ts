import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DisplaytransactionsComponent } from './displaytransactions.component';

describe('DisplaytransactionsComponent', () => {
  let component: DisplaytransactionsComponent;
  let fixture: ComponentFixture<DisplaytransactionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DisplaytransactionsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DisplaytransactionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
