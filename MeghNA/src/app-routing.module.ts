import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CloudDetectComponent } from './app/cloud-detect/cloud-detect.component';
import { CloudMotionPredictComponent } from './app/cloud-motion-predict/cloud-motion-predict.component';

/**
 * Below array handles routing for
 * the web-app
 */
const routes: Routes = [
  { path:'', pathMatch:'full', redirectTo:'detect' },
  { path:'detect', component:CloudDetectComponent },
  { path:'predict', component:CloudMotionPredictComponent }
]

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { onSameUrlNavigation: 'reload' })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
