import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { Metadata } from '../../model/metadata';
import { MetadataService } from '../../services/metadata.service';

@Component({
  selector: 'app-metadata',
  templateUrl: './metadata.component.html',
  styleUrl: './metadata.component.css'
})
export class MetadataComponent implements OnChanges {

  metadata: Metadata;
  isLoading = false;
  @Input() selectedFileId: string | undefined;

  constructor(private metadataService: MetadataService) { }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['selectedFileId'] && changes['selectedFileId'].currentValue) {
      this.fetchMetadata(changes['selectedFileId'].currentValue);
    }
  }

  fetchMetadata(selectedFileId: string) {
    this.getMetadata(selectedFileId);
    const fileContainer =  document.getElementById('fileContainer');
    if (fileContainer) {
      fileContainer.innerHTML = '';
    }
    this.metadataService.getBlobFile(Number(selectedFileId)).subscribe((response) => {
      const fileType = response.file_type;  // e.g., 'application/pdf', 'audio/mp3'
      const fileData = response.file_data;  // Base64 encoded data

      // Create an object URL for the base64 data
      const fileURL = `data:${fileType};base64,${fileData}`;

      if (fileType.startsWith('image')) {
        // For images
        const img = document.createElement('img');
        img.src = fileURL;
        img.style.width = '100%';
        img.style.height = 'auto';
        fileContainer.appendChild(img);
      } else if (fileType.startsWith('video') || fileType.startsWith('audio')) {
        // For video or audio
        const mediaElement = document.createElement(fileType.startsWith('video') ? 'video' : 'audio');
        mediaElement.src = fileURL;
        mediaElement.controls = true;
        mediaElement.style.width = '100%';
        mediaElement.style.height = 'auto';
        fileContainer.appendChild(mediaElement);
      } else if (fileType === 'application/pdf') {
        // For PDFs
        const iframe = document.createElement('iframe');
        iframe.src = fileURL;
        iframe.style.width = '100%';
        iframe.style.height = '500px'; // Adjust as needed
        fileContainer.appendChild(iframe);
      }
    });
  }

  private getMetadata(id: string) {
    this.isLoading = true;
    this.metadataService.getFile(id).subscribe(
      res => {
        this.metadata = res;
        this.isLoading = false;
      }
    );
  }
}
