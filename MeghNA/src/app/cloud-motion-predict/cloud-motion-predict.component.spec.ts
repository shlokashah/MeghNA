import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CloudMotionPredictComponent } from './cloud-motion-predict.component';

describe('CloudMotionPredictComponent', () => {
  let component: CloudMotionPredictComponent;
  let fixture: ComponentFixture<CloudMotionPredictComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CloudMotionPredictComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CloudMotionPredictComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
