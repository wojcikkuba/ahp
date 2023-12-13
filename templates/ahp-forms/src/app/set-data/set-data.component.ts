import { Component, inject } from '@angular/core';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { MatChipInputEvent } from '@angular/material/chips';
import { Router } from '@angular/router';
import { SettedData } from '../interfaces';
import { AppService } from '../app.service';

@Component({
  selector: 'app-set-data',
  templateUrl: './set-data.component.html',
  styleUrls: ['./set-data.component.scss']
})
export class SetDataComponent {
  separatorKeysCodes: number[] = [ENTER, COMMA];
  criteria: string[] = [];
  variants: string[] = [];
  inputName!: string;

  announcer = inject(LiveAnnouncer);

  constructor(
    private router: Router,
    private appService: AppService
  ) {}

  add(event: MatChipInputEvent, formNum: number): void {
    const value = (event.value || '').trim();
    if (value && formNum === 1) {
      this.criteria.push(value);
    }
    if (value && formNum === 2) {
      this.variants.push(value);
    }
    event.chipInput!.clear();
  }

  remove(item: string, formNum: number): void {
    const index = this.criteria.indexOf(item);
    const index2 = this.variants.indexOf(item);

    if (index >= 0 && formNum === 1) {
      this.criteria.splice(index, 1);
      this.announcer.announce(`Removed ${item}`);
    }
    if (index2 >= 0 && formNum === 2) {
      this.variants.splice(index2, 1);
      this.announcer.announce(`Removed ${item}`);
    }
  }

  startFilling(): void {
    const checkInputData: boolean = !!this.inputName && this.criteria.length > 0 && this.variants.length > 0;
    const data: SettedData = {
      name: this.inputName,
      criteria: this.criteria,
      variants: this.variants
    } 
    if (checkInputData) {
      this.appService.sendData(data);
      this.router.navigate(['compare']);
    }
  }
}
