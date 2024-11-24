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

  constructor(private metadataService: MetadataService, private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      this.metadataService.getFile(id).subscribe(
        res => {
          this.metadata = res;
        }
      )
    });
  }

}
