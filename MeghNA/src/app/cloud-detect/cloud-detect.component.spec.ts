import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CloudDetectComponent } from './cloud-detect.component';

describe('CloudDetectComponent', () => {
  let component: CloudDetectComponent;
  let fixture: ComponentFixture<CloudDetectComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CloudDetectComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CloudDetectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
