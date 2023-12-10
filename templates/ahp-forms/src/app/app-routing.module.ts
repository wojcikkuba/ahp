import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SetDataComponent } from './set-data/set-data.component';
import { CompareComponent } from './compare/compare.component';
import { ResultsComponent } from './results/results.component';

const routes: Routes = [
  { path: 'set-data', component: SetDataComponent },
  { path: 'compare', component: CompareComponent },
  { path: 'results', component: ResultsComponent },
  { path: '**', redirectTo: 'set-data' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule { }
