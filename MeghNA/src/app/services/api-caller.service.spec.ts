import { TestBed, inject } from '@angular/core/testing';

import { ApiCallerService } from './api-caller.service';

describe('ApiCallerService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ApiCallerService]
    });
  });

  it('should be created', inject([ApiCallerService], (service: ApiCallerService) => {
    expect(service).toBeTruthy();
  }));
});
