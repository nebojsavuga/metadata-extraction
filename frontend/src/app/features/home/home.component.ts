import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environment/environment';
import { MetadataService } from '../../services/metadata.service';
import { Metadata } from '../../model/metadata';
import { UploadedFile } from '../../model/file';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {
  selectedFile: File | null = null;
  isLoading: boolean = false;
  fileName: string | null = null;
  metadata: Metadata;
  files: UploadedFile[] = [];

  constructor(private metadataService: MetadataService) { }

  ngOnInit(): void {
    this.getFiles();

    this.metadataService.getFolders().subscribe(
      res =>{
        console.log(res);
      }
    )
  }

  getFiles() {
    this.isLoading = true;
    this.metadataService.getFiles().subscribe(
      res => {
        this.files = res;
        this.isLoading = false;
      }
    );
  }

  onFileChange(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.fileName = file.name;
    }
  }

  uploadFile(): void {
    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('file', this.selectedFile, this.selectedFile.name);

      this.uploadToServer(formData);
    }
  }

  uploadToServer(formData: FormData) {
    this.isLoading = true;
    this.metadataService.uploadFile(formData).subscribe(
      {
        next: res => {
          this.isLoading = false;
          this.metadata = res;
          this.getFiles();
        },

        error: err => {
          this.isLoading = false;
        }
      }
    );
  }
}
