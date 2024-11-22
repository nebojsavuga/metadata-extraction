import { Injectable } from '@angular/core';
import { environment } from '../../environment/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MetadataService {
  baseUrl: string = environment.apiHost;

  constructor(private http: HttpClient) { }

  uploadFile(formData: FormData): Observable<any> {
    const url = environment.apiHost;
    return this.http.post(url, formData);
  }
}
