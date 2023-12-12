import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { FormResultData, PostAnswers, SettedData } from './interfaces';
import { HttpClient, HttpHeaders } from '@angular/common/http';

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

  constructor(private http: HttpClient) { }

  sendData(data: SettedData) {
    this.dataSubject.next(data);
  }

  postResults(answers: PostAnswers): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    });
  
    return this.http.post(`http://127.0.0.1:5000/calculate`, answers, { headers });
  }
  

  getResults(): Observable<FormResultData[]> {
    return this.http.get<FormResultData[]>(`http://127.0.0.1:5000/data`);
  }
}
