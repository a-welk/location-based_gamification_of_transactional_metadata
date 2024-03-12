import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TransactionService {

  private apiUrl = 'http://127.0.0.1:5000/getTransactions';

  constructor(private http: HttpClient) { }

  fetchData(): Observable<any> {
    return this.http.get(this.apiUrl);
  }
}