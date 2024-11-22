import { Component, Input } from '@angular/core';
import { Metadata } from '../../model/metadata';

@Component({
  selector: 'app-metadata',
  templateUrl: './metadata.component.html',
  styleUrl: './metadata.component.css'
})
export class MetadataComponent {

  @Input() metadata: Metadata;
  
}
