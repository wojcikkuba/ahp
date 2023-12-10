import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { PostAnswers, SettedData } from './interfaces';
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
      'Accept' : '*/*',
      'Content-Type' : 'application/json',
    });
    
    return this.http.post(`http://127.0.0.1:5000/calculate`, answers, { headers: headers });
  }
}
