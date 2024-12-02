import { Injectable } from '@angular/core';
import { environment } from '../../environment/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
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

  deleteFile(file_id: number): Observable<any> {
    const url = environment.apiHost;
    return this.http.delete<any>(url + file_id);
  }

  getBlobFile(file_id: number): Observable<any> {
    const url = `${environment.apiHost}file/${file_id}`;
    return this.http.get(url);
  }
  editMetadata(metadata: Metadata, file_id:string): Observable<any> {
    const url = `${environment.apiHost}/${file_id}`; // Dodaj ID datoteke
    const headers = new HttpHeaders({
        'Content-Type': 'application/json'
    });
    console.log((url));
    return this.http.put(url, metadata);
}
}
