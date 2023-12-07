import { Component, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { AppService } from '../app.service';
import { Subscription } from 'rxjs';
import { SettedData, FormAnswer } from '../interfaces';

@Component({
  selector: 'app-compare',
  templateUrl: './compare.component.html',
  styleUrls: ['./compare.component.scss']
})
export class CompareComponent implements OnDestroy {
  private dataSubscription!: Subscription;
  receivedData!: SettedData;
  comparisonValues: number[][][] = [];
  formAnswers: FormAnswer[] = [];
  value: number = 50;

  constructor(
    private router: Router,
    private appService: AppService
  ) {}

  ngAfterViewInit(): void {
    this.takeUserData();
  }

  ngOnDestroy(): void {
    this.dataSubscription.unsubscribe();
  }

  takeUserData(): void {
    this.dataSubscription = this.appService.data$.subscribe((data) => {
      this.receivedData = data;

      this.comparisonValues = new Array(this.receivedData.criteria.length)
        .fill([])
        .map(() => new Array(this.receivedData.variants.length)
          .fill([])
          .map(() => new Array(this.receivedData.variants.length).fill(50))); // Default value is 50
    });

    if (!this.receivedData.name) {
      this.router.navigate(['set-data']);
    }
  }

  submitComparisonResults(): void {
    this.formAnswers = [];

    for (let cIndex = 0; cIndex < this.receivedData.criteria.length; cIndex++) {
        for (let i = 0; i < this.receivedData.variants.length; i++) {
            for (let j = i + 1; j < this.receivedData.variants.length; j++) {
                const variant1 = this.receivedData.variants[i];
                const variant2 = this.receivedData.variants[j];
                const count = this.comparisonValues[cIndex][i][j];

                const formAnswer: FormAnswer = {
                    criterion: this.receivedData.criteria[cIndex],
                    varinatOne: variant1,
                    variantTwo: variant2,
                    count: count,
                };

                this.formAnswers.push(formAnswer);
            }
        }
    }
    console.log('Comparison results:', this.formAnswers);
  }
}
