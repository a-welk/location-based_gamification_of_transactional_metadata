import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TransactionService {

  private baseUrl = 'http://127.0.0.1:5000/1/transactions';  // URL to web API

  constructor(private http: HttpClient) { }

  getTransactions(): Observable<any> {
    return this.http.get<any>(this.baseUrl);
  }
}
