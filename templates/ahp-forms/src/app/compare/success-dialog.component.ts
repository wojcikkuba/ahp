import { Component, EventEmitter, Inject, Output } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-success-dialog',
  template: `
    <div class="success-dialog-container">
      <h2 *ngIf="data.error" style="color: red;">!!! {{data.errorMessage.error}} !!!</h2>
      <h2>Thank you for completing the survey!</h2>
      <p>Your responses have been successfully submitted.</p>
      <button mat-raised-button color="primary" (click)="closeDialog()">Close</button>
    </div>
  `,
  styles: [`
    .success-dialog-container {
      text-align: center;
      padding: 20px;
      background-color: black;
      color: #00FFFF;
      border-radius: 8px;
      box-shadow: 0px 0px 10px rgba(0, 255, 255, 0.5);
    }

    h2 {
      margin-bottom: 10px;
    }

    button {
      margin-top: 20px;
    }
  `],
})
export class SuccessDialogComponent {
  @Output() dialogClosed = new EventEmitter<void>();

  constructor(
    public dialogRef: MatDialogRef<SuccessDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { error: boolean, errorMessage: any }
  ) {}

  closeDialog(): void {
    this.dialogClosed.emit();
    this.dialogRef.close();
  }
}