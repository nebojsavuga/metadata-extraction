import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MetadataFolder, UploadedFile } from '../../model/file';
import { MetadataService } from '../../services/metadata.service';
import { SnackbarService } from '../../services/snackbar.service';

@Component({
  selector: 'app-files',
  templateUrl: './files.component.html',
  styleUrl: './files.component.css'
})
export class FilesComponent {

  @Input() files: UploadedFile[] = [];
  @Input() folders: MetadataFolder[] = [];
  @Output() refresh = new EventEmitter<boolean>();
  isLoading: boolean = false;
  selectedFileId: number | undefined;
  selectedFolderId: number | null = null;

  constructor(private metadataService: MetadataService, private snackbar: SnackbarService) { }

  onFileClick(event: any) {
    if (this.selectedFileId === event) {
      this.selectedFileId = null;
    } else {
      this.selectedFileId = event;
    }
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
      case 'jpg':
      case 'jpeg':
      case 'png':
        return 'bi bi-file-earmark-image-fill';
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

  onAddFolderClick() {
    const folderName = prompt('Enter folder name');
    const exists = this.folders.findIndex(x => x.name === folderName && x.parent_folder_id === this.selectedFolderId) != -1;
    if (exists) {
      this.snackbar.showSnackBar('File with this name already exists.', 'Ok.');
      return;
    }
    if (folderName) {
      this.metadataService.createFolder(folderName, this.selectedFolderId).subscribe(
        {
          next: newFolder => {
            this.folders.push(newFolder);
            this.loadFiles();
          },
          error: err => {
            console.error('Error creating folder:', err);
          }
        }
      );
    }
  }

  onDeleteFolderClick(folderId: number) {
    if (confirm('Are you sure you want to delete this folder?')) {
      this.metadataService.deleteFolder(folderId).subscribe(
        {
          next: () => {
            this.folders = this.folders.filter(x => x.id !== folderId);
            this.selectedFolderId = null;
            this.loadFiles();
          },
          error: err => {
            console.error('Error deleting folder:', err);
          }
        }
      );
    }
  }

  loadFiles() {
    this.isLoading = true;
    this.metadataService.getFiles().subscribe(
      {
        next: files => {
          this.files = files;
          this.isLoading = false;
        },
        error: err => {
          console.error('Error loading files:', err);
          this.isLoading = false;
        }
      }
    );
  }

  onFolderClick(id: number) {
    if (this.selectedFolderId === id) {
      this.selectedFolderId = null;
    } else {
      this.selectedFolderId = id;
    }
  }
}
