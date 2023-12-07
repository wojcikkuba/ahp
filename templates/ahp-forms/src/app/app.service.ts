import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';
import { SettedData } from './interfaces';

@Injectable({
  providedIn: 'root'
})
export class AppService {
  private dataSubject = new BehaviorSubject<SettedData>({
    name: '',
    criteria: [],
    variants: []
  });
  public data$ = this.dataSubject.asObservable();

  sendData(data: SettedData) {
    this.dataSubject.next(data);
  }
}
