import { Component, EventEmitter, Input, Output } from '@angular/core';
import { UploadedFile } from '../../model/file';
import { Router } from '@angular/router';
import { MetadataService } from '../../services/metadata.service';
import { SnackbarService } from '../../services/snackbar.service';

@Component({
  selector: 'app-files',
  templateUrl: './files.component.html',
  styleUrl: './files.component.css'
})
export class FilesComponent {

  @Input() files: UploadedFile[] = [];
  @Output() refresh = new EventEmitter<boolean>();
  isLoading: boolean = false;

  constructor(private router: Router, private metadataService: MetadataService, private snackbar: SnackbarService) { }

  onFileClick(event: any) {
    this.router.navigate(['file/' + event])
  }

  getFileIcon(fileName: string): string {
    const fileExtension = fileName.split('.').pop()?.toLowerCase();
    switch (fileExtension) {
      case 'pdf':
        return 'bi bi-file-earmark-pdf-fill';
      case 'doc':
      case 'docx':
        return 'bi bi-file-earmark-word-fill';
      case 'xls':
      case 'xlsx':
        return 'bi bi-file-earmark-excel-fill';
      case 'mp3':
        return 'bi bi-file-earmark-music-fill';
      case 'mp4':
      case 'mov':
        return 'bi bi-file-earmark-play-fill';
      default:
        return 'bi bi-file-earmark-fill';
    }
  }

  onDeleteClick(fileId: number): void {
    this.isLoading = true;
    this.metadataService.deleteFile(fileId).subscribe(
      {
        next: () => {
          this.refresh.emit(true);
          this.snackbar.showSnackBar('Successfully deleted file.', 'Ok');
          this.isLoading = false;
        },
        error: () => {
          this.snackbar.showSnackBar('Something went wrong', 'Ok');
          this.isLoading = false;
        }
      }
    )
  }
}
