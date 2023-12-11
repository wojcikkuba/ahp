import { Component, OnDestroy, OnInit, QueryList, ViewChildren } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatExpansionPanel } from '@angular/material/expansion';
import { FormResultData } from '../interfaces';
import { AppService } from '../app.service';
import { HttpErrorResponse } from '@angular/common/http';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss']
})
export class ResultsComponent implements OnInit, OnDestroy {
  @ViewChildren(MatExpansionPanel) panels!: QueryList<MatExpansionPanel>;
  private dataSubscription!: Subscription;

  forms!: FormResultData[];
  // 

  Object = Object;

  constructor(
    public dialog: MatDialog,
    private appService: AppService,
  ) {}

  ngOnInit(): void {
    this.getAllForms();
  }

  ngOnDestroy(): void {
    this.dataSubscription.unsubscribe();
  }

  togglePanel(clickedPanel: MatExpansionPanel): void {
    this.panels.forEach(panel => {
      if (panel !== clickedPanel && panel.expanded) {
        panel.close();
      }
    });
  }

  getAllForms(): void {
    this.dataSubscription = this.appService.getResults()
      .subscribe(
        (response) => {
          console.log(response);
          this.forms = response;
        },
        (error: HttpErrorResponse) => {
          console.error(error);
        }
      );
  }
}
