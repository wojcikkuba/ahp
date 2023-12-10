import { Component, QueryList, ViewChildren } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatExpansionPanel } from '@angular/material/expansion';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss']
})
export class ResultsComponent {
  @ViewChildren(MatExpansionPanel) panels!: QueryList<MatExpansionPanel>;

  forms: string[] = ["1", "2", "3"];
  matrix: number[][] = [
    [0.3, 0.5, 0.2],
    [0.4, 0.3, 0.3],
    [0.2, 0.2, 0.6]
  ];
  receivedData: any = {
    variants: ["V1", "V2", "V3"],
    criteria: ["C1", "C2", "C3"]
  }

  constructor(
    
  ) {}

  togglePanel(clickedPanel: MatExpansionPanel): void {
    this.panels.forEach(panel => {
      if (panel !== clickedPanel && panel.expanded) {
        panel.close();
      }
    });
  }
}
