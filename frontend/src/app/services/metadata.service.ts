import { Injectable } from '@angular/core';
import { environment } from '../../environment/environment';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { Metadata } from '../model/metadata';
import { MetadataFolder, UploadedFile } from '../model/file';

@Injectable({
  providedIn: 'root'
})
export class MetadataService {

  baseUrl: string = environment.apiHost;

  constructor(private http: HttpClient) { }

  uploadFile(formData: FormData): Observable<Metadata> {
    return this.http.post<Metadata>(this.baseUrl, formData);
  }

  getFiles(): Observable<UploadedFile[]> {
    return this.http.get<UploadedFile[]>(this.baseUrl);
  }

  getFile(file_id: string): Observable<Metadata> {
    return this.http.get<Metadata>(this.baseUrl + Number(file_id));
  }

  deleteFile(file_id: number): Observable<any> {
    return this.http.delete<any>(this.baseUrl + file_id);
  }

  getBlobFile(file_id: number): Observable<any> {
    const url = `${this.baseUrl}file/${file_id}`;
    return this.http.get(url);
  }

  getFolders(): Observable<MetadataFolder[]> {
    const url = `${this.baseUrl}folders`;
    return this.http.get<MetadataFolder[]>(url);
  }

  createFolder(name: string, parentFolderId?: number): Observable<MetadataFolder> {
    const url = `${this.baseUrl}folders`;
    const body = { name, parent_folder_id: parentFolderId };
    return this.http.post<MetadataFolder>(url, body);
  }

  deleteFolder(folderId: number): Observable<any> {
    const url = `${this.baseUrl}folders/${folderId}`;
    return this.http.delete<any>(url);
  }

}
