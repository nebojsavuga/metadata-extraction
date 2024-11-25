import { Component, Input, OnInit } from '@angular/core';
import { Metadata } from '../../model/metadata';
import { MetadataService } from '../../services/metadata.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-metadata',
  templateUrl: './metadata.component.html',
  styleUrl: './metadata.component.css'
})
export class MetadataComponent implements OnInit {

  metadata: Metadata;
  isLoading = false;
  constructor(private metadataService: MetadataService, private route: ActivatedRoute) { }

  ngOnInit(): void {

    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      this.getMetadata(id);

      this.metadataService.getBlobFile(Number(id)).subscribe((response) => {
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
          document.getElementById('fileContainer').appendChild(img);
        } else if (fileType.startsWith('video') || fileType.startsWith('audio')) {
          // For video or audio
          const mediaElement = document.createElement(fileType.startsWith('video') ? 'video' : 'audio');
          mediaElement.src = fileURL;
          mediaElement.controls = true;
          mediaElement.style.width = '100%';
          mediaElement.style.height = 'auto';
          document.getElementById('fileContainer').appendChild(mediaElement);
        } else if (fileType === 'application/pdf') {
          // For PDFs
          const iframe = document.createElement('iframe');
          iframe.src = fileURL;
          iframe.style.width = '100%';
          iframe.style.height = '500px'; // Adjust as needed
          document.getElementById('fileContainer').appendChild(iframe);
        }
      })
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
