import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { AppRoutingModule } from '../app-routing.module';
import { NavbarComponent } from './navbar/navbar.component';
import { CloudDetectComponent } from './cloud-detect/cloud-detect.component';
import { CloudMotionPredictComponent } from './cloud-motion-predict/cloud-motion-predict.component';

import { NgxSpinnerModule } from 'ngx-spinner';
import { ApiCallerService } from './services/api-caller.service';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    CloudDetectComponent,
    CloudMotionPredictComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgxSpinnerModule,
    FormsModule,
    HttpModule
  ],
  providers: [ApiCallerService],
  bootstrap: [AppComponent]
})
export class AppModule { }
