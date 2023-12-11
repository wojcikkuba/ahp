import { Component, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { AppService } from '../app.service';
import { Subscription } from 'rxjs';
import { SettedData, FormAnswer, PostAnswers } from '../interfaces';
import { MatDialog } from '@angular/material/dialog';
import { SuccessDialogComponent } from './success-dialog.component';
import { HttpErrorResponse } from '@angular/common/http';

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
  value: number = 8;
  stepIndex: number = 0;
  steps: number[] = [1/9, 1/8, 1/7, 1/6, 1/5, 1/4, 1/3, 1/2, 1, 2, 3, 4, 5, 6, 7, 8, 9];

  constructor(
    private router: Router,
    private appService: AppService,
    private dialog: MatDialog
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
          .map(() => new Array(this.receivedData.variants.length).fill(8)));
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
                    varinat1: variant1,
                    variant2: variant2,
                    count: this.steps[count],
                };

                this.formAnswers.push(formAnswer);
            }
        }
    }
    console.log('Comparison results:', this.formAnswers);
    this.postResults(this.formAnswers);
  }

  postResults(answers: FormAnswer[]): void {
    const postAnswers: PostAnswers = {
      userName: this.receivedData.name,
      answers: answers
    };
  
    console.log(postAnswers);
  
    this.appService.postResults(postAnswers)
      .subscribe(
        (response) => {
          console.log(response);
          const dialogRef = this.dialog.open(SuccessDialogComponent);
  
          dialogRef.componentInstance.dialogClosed.subscribe(() => {
            this.router.navigate(['set-data']);
          });
        },
        (error: HttpErrorResponse) => {
          console.error(error);
  
          const dialogRef = this.dialog.open(SuccessDialogComponent, {
            data: { error: true, errorMessage: error.error}
          });
  
          dialogRef.componentInstance.dialogClosed.subscribe(() => {
            this.router.navigate(['set-data']);
          });
        }
      );
  }
}
