import { Component, QueryList, ViewChildren } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatExpansionPanel } from '@angular/material/expansion';
import { FormResultData } from '../interfaces';
import { AppService } from '../app.service';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss']
})
export class ResultsComponent {
  @ViewChildren(MatExpansionPanel) panels!: QueryList<MatExpansionPanel>;

  forms: FormResultData[] = [
    {
      ankieta: "Ankieta 1",
      kategorie: ["cena", "wyglad", "moc"],
      warianty: ["audi", "vw", "skoda"],
      najlepszy_wariant: {
        "cena": 2,
        "wyglad": 1,
        "moc": 2
      },
      wyniki: [
        {
          uzytkownik: "bartek",
          oceny: {
            "cena": [0.3, 0.5, 0.2],
            "wyglad": [0.4, 0.4, 0.2],
            "moc": [0.25, 0.5, 0.25]
          },
          is_consistent: true
        }
      ],
      scores: [1.05, 0.95, 1.1]
    },
    {
      ankieta: "Ankieta 2",
      kategorie: ["smak", "wyglad", "zapach"],
      warianty: ["spaghetti", "pizza", "pasta"],
      najlepszy_wariant: {
        "smak": 2,
        "wyglad": 1,
        "zapach": 0
      },
      wyniki: [
        {
          uzytkownik: "bartek",
          oceny: {
            "smak": [0.5, 0.2, 0.3],
            "wyglad": [0.4, 0.3, 0.3],
            "zapach": [0.3, 0.4, 0.3]
          },
          is_consistent: true
        }
      ],
      scores: [1.2, 0.8, 1.0]
    }
  ];

  Object = Object;

  constructor(
    public dialog: MatDialog,
    private appService: AppService,
  ) {}

  togglePanel(clickedPanel: MatExpansionPanel): void {
    this.panels.forEach(panel => {
      if (panel !== clickedPanel && panel.expanded) {
        panel.close();
      }
    });
  }

  // getAllForms(): void {
  //   this.appService.getResults()
  //     .subscribe(
  //       (response) => {
  //         console.log(response);
  //         this.forms = response;
  //       },
  //       (error: HttpErrorResponse) => {
  //         console.error(error);
  //       }
  //     );
  // }
}
