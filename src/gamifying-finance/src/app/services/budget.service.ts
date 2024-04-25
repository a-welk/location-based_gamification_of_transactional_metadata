import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BudgetService {

  private backendUrl = 'http://127.0.0.1:5000/getAverages';

  constructor(private http: HttpClient) { }

  getAverageData(month: String, year: String, zipcode: number): Observable<any> {
    let params = new HttpParams()
      .set('month', month.toString())
      .set('year', year.toString())
      .set('zipcode', zipcode.toString());

    return this.http.get<any>(this.backendUrl, { params });
  }
}
