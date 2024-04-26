import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CategoriesLeaderboardComponent } from './categories-leaderboard.component';

describe('CategoriesLeaderboardComponent', () => {
  let component: CategoriesLeaderboardComponent;
  let fixture: ComponentFixture<CategoriesLeaderboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CategoriesLeaderboardComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CategoriesLeaderboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
