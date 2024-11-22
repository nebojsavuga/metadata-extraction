import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environment/environment';
import { MetadataService } from '../../services/metadata.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  selectedFile: File | null = null;
  isLoading: boolean = false;

  constructor(private metadataService: MetadataService) { }

  onFileChange(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
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
          console.log(res);
        },

        error: err => {
          this.isLoading = false;
          console.log(err);
        }
      }
    );
  }
}
