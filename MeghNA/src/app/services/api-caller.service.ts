import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { RequestOptions, Headers, Http, Response } from '@angular/http';

@Injectable({
  providedIn: 'root'
})
export class ApiCallerService {

  private baseUrl = "http://76eac9623e94.ngrok.io";

  constructor(private http: Http) { }

  doGetRequest(url:string): Observable<any> {
    let options: RequestOptions = new RequestOptions({
      headers: new Headers({ 'Content-Type': 'application/json' })
    });
    url = this.baseUrl + url;
    return this.http.get(url, options).pipe(map((res:Response) => res.json()));
  }

  doPostRequest(url:string, postBody: any):Observable<any> {
    let options: RequestOptions = new RequestOptions({
      headers: new Headers({ 'Content-Type': 'application/json' })
    });
    url = this.baseUrl + url;
    return this.http.post(url, postBody, options).pipe(map((res:Response) => res.json()));
  }

}