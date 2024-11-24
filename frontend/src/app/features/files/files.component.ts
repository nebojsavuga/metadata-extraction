import { Component, Input } from '@angular/core';
import { UploadedFile } from '../../model/file';

@Component({
  selector: 'app-files',
  templateUrl: './files.component.html',
  styleUrl: './files.component.css'
})
export class FilesComponent {

  @Input() files: UploadedFile[] = [];

  onFileClick(event: any) {
    console.log(event);
  }

  getFileIcon(fileName: string): string {
    const fileExtension = fileName.split('.').pop()?.toLowerCase();
    switch (fileExtension) {
      case 'pdf':
        return 'bi bi-file-earmark-pdf-fill'; // PDF icon
      case 'doc':
      case 'docx':
        return 'bi bi-file-earmark-word-fill'; // Word icon
      case 'xls':
      case 'xlsx':
        return 'bi bi-file-earmark-excel-fill'; // Excel icon
      case 'mp3':
        return 'bi bi-file-earmark-music-fill'; // Music icon
      case 'mp4':
      case 'mov':
        return 'bi bi-file-earmark-play-fill'; // Video icon
      default:
        return 'bi bi-file-earmark-fill'; // Default file icon
    }
  }
}
