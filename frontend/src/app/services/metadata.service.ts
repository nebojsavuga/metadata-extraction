import { Injectable } from '@angular/core';
import { environment } from '../../environment/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Metadata } from '../model/metadata';
import { MetadataFolder, UploadedFile } from '../model/file';

@Injectable({
  providedIn: 'root'
})
export class MetadataService {

  baseUrl: string = environment.apiHost;

  constructor(private http: HttpClient) { }

  uploadFile(formData: FormData, folderId: number | undefined): Observable<Metadata> {
    const url = `${this.baseUrl.replace(/\/$/, '')}?folderId=${folderId}`;
    return this.http.post<Metadata>(url, formData);
  }

  getFiles(): Observable<UploadedFile[]> {
    return this.http.get<UploadedFile[]>(this.baseUrl);
  }

  getFile(file_id: number): Observable<Metadata> {
    return this.http.get<Metadata>(this.baseUrl + file_id);
  }

  deleteFile(file_id: number): Observable<any> {
    return this.http.delete<any>(this.baseUrl + file_id);
  }

  getBlobFile(file_id: number): Observable<any> {
    const url = `${this.baseUrl}file/${file_id}`;
    return this.http.get(url);
  }
  editMetadata(metadata: Metadata, file_id: number): Observable<any> {
    const url = `${environment.apiHost}/${file_id}`; // Dodaj ID datoteke
    return this.http.put(url, metadata);
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
