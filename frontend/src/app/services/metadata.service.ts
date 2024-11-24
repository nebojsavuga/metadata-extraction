import { Injectable } from '@angular/core';
import { environment } from '../../environment/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Metadata } from '../model/metadata';
import { UploadedFile } from '../model/file';

@Injectable({
  providedIn: 'root'
})
export class MetadataService {
  baseUrl: string = environment.apiHost;

  constructor(private http: HttpClient) { }

  uploadFile(formData: FormData): Observable<Metadata> {
    const url = environment.apiHost;
    return this.http.post<Metadata>(url, formData);
  }

  getFiles(): Observable<UploadedFile[]> {
    const url = environment.apiHost;
    return this.http.get<UploadedFile[]>(url);
  }

  getFile(file_id: string): Observable<Metadata> {
    const url = environment.apiHost;
    return this.http.get<Metadata>(url + Number(file_id));
  }
}
