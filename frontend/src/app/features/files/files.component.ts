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


  _folders: MetadataFolder[];
  _files: UploadedFile[];

  @Input() set files(files: UploadedFile[]) {
    this._files = files;

    this.filterFiles(this.selectedFolderId);

  }

  get files() {
    return this._files;
  }

  @Input() set folders(folders: MetadataFolder[]) {
    this._folders = folders;
    this.filterFolders(this.selectedFolderId);
  }

  get folders() {
    return this._folders;
  }

  @Input() displayedFolders: MetadataFolder[] = [];
  @Input() displayedFiles: UploadedFile[] = [];
  @Output() refresh = new EventEmitter<boolean>();
  @Output() selectedFolder = new EventEmitter<number>();
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
    const exists = this.displayedFolders.findIndex(x => x.name === folderName && x.parent_folder_id === this.selectedFolderId) != -1;
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
            this.filterFolders(newFolder.parent_folder_id);
          },
          error: err => {
            console.error('Error creating folder:', err);
          }
        }
      );
    }
  }

  onDeleteFolderClick(folderId: number) {
    const hasItems = this.folders.find(x => x.parent_folder_id === folderId) !== undefined || this.files.find(x => x.folder_id === folderId) !== undefined;
    if (hasItems) {
      this.snackbar.showSnackBar('Can\'t delete a folder which has objects in it.', 'Ok');
      return;
    }
    if (confirm('Are you sure you want to delete this folder?')) {
      this.metadataService.deleteFolder(folderId).subscribe(
        {
          next: () => {
            const parent_folder_id = this.folders.find(x => x.id === folderId).parent_folder_id;
            this.folders = this.folders.filter(x => x.id !== folderId);
            this.filterFolders(parent_folder_id);
            this.selectedFolderId = parent_folder_id;
            this.selectedFolder.emit(this.selectedFolderId);
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
    this.selectedFolder.emit(this.selectedFolderId);
    this.filterFolders(id);
    this.filterFiles(id);
  }

  filterFolders(folderId: number | undefined = undefined) {
    this.displayedFolders = this.folders.filter(x => x.parent_folder_id === folderId);
  }

  filterFiles(folder_id: number | undefined = undefined) {
    this.displayedFiles = this.files.filter(x => x.folder_id === folder_id);
  }

  onBackFolder() {
    const folder = this.folders.find(x => x.id === this.selectedFolderId);
    this.filterFiles(folder.parent_folder_id);
    this.filterFolders(folder.parent_folder_id);
    this.selectedFolderId = folder.parent_folder_id;
    this.selectedFolder.emit(this.selectedFolderId);
  }
}
