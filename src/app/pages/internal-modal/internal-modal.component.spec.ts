import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InternalModalComponent } from './internal-modal.component';

describe('InternalModalComponent', () => {
  let component: InternalModalComponent;
  let fixture: ComponentFixture<InternalModalComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [InternalModalComponent]
    });
    fixture = TestBed.createComponent(InternalModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
