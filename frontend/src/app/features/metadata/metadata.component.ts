import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import {
  ClassificationMetadata, EducationalMetadata, GeneralMetadata, LifeCycleMetadata, Metadata,
  RelationMetadata, RightsMetadata, TehnicalMetadata
} from '../../model/metadata';

import { MetadataService } from '../../services/metadata.service';
import { FormControl, FormGroup } from '@angular/forms';
import {
  interactivityLevels, learningResourceTypes, semanticDensities,
  intendedUserRoles,
  contexts,
  difficulties,
  aggregationLevels,
  structures,
  purposes,
  interactivityTypes
} from '../../model/lists';

@Component({
  selector: 'app-metadata',
  templateUrl: './metadata.component.html',
  styleUrl: './metadata.component.css'
})
export class MetadataComponent implements OnChanges {

  metadata: Metadata;
  isLoading = false
  interactivityLevels: string[] = interactivityLevels;
  learningResourceTypes: string[] = learningResourceTypes;
  semanticDensities: string[] = semanticDensities;
  intendedUserRoles: string[] = intendedUserRoles;
  contexts: string[] = contexts;
  difficulties: string[] = difficulties;
  aggregationLevels: string[] = aggregationLevels;
  structures: string[] = structures;
  purposes: string[] = purposes;
  interactivityTypes: string[] = interactivityTypes;
  constructor(private metadataService: MetadataService) { }

  metadataForm = new FormGroup({
    id: new FormControl(''),
    general_title: new FormControl(''),
    general_description: new FormControl(''),
    general_coverage: new FormControl(''),
    general_aggregation_level: new FormControl(''),
    general_keywords: new FormControl(''),
    general_language: new FormControl(''),
    general_structure: new FormControl(''),
    educational_interactivity_type: new FormControl(''),
    educational_learning_resource_type: new FormControl(''),
    educational_interactivity_level: new FormControl(''),
    educational_semantic_density: new FormControl(''),
    educational_intended_end_user_role: new FormControl(''),
    educational_context: new FormControl(''),
    educational_typical_age_range: new FormControl(''),
    educational_difficulty: new FormControl(''),
    educational_stypical_learning_time: new FormControl(''),
    educational_description: new FormControl(''),
    educational_language: new FormControl(''),
    lifeCycle_version: new FormControl(''),
    lifeCycle_status: new FormControl(''),
    lifeCycle_contribute: new FormControl(''),
    classification_purpose: new FormControl(''),
    classification_taxon_path: new FormControl(''),
    classification_description: new FormControl(''),
    classification_keywords: new FormControl(''),
    rights_cost: new FormControl(''),
    rights_copyright: new FormControl(''),
    rights_description: new FormControl(''),
    relation_kind: new FormControl(''),
    relation_resource: new FormControl(''),
    relation_annotation: new FormControl(''),
    technical_format: new FormControl(''),
    technical_size: new FormControl(''),
    technical_location: new FormControl(''),
    technical_requirement: new FormControl(''),
    technical_installation_remarks: new FormControl(''),
    technical_duration: new FormControl(''),
  });
  @Input() selectedFileId: number | undefined;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['selectedFileId'] && changes['selectedFileId'].currentValue) {
      this.fetchMetadata(changes['selectedFileId'].currentValue);
    }
  }

  fetchMetadata(selectedFileId: number) {
    this.getMetadata(selectedFileId);
    const fileContainer = document.getElementById('fileContainer');
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

  editMetadata() {
    if (!this.metadataForm.valid) {
      return;
    }
    let general: GeneralMetadata = {
      id: this.metadataForm.value.id,
      title: this.metadataForm.value.general_title,
      description: this.metadataForm.value.general_description,
      language: this.metadataForm.value.general_language,
      keywords: this.metadataForm.value.general_keywords,
      structure: this.metadataForm.value.general_structure,
      coverage: this.metadataForm.value.general_coverage,
      aggregation_level: this.metadataForm.value.general_aggregation_level,
    }
    let educational: EducationalMetadata = {
      interactivity_type: this.metadataForm.value.educational_interactivity_type,
      learning_resource_type: this.metadataForm.value.educational_learning_resource_type,
      interactivity_level: this.metadataForm.value.educational_interactivity_level,
      semantic_density: this.metadataForm.value.educational_semantic_density,
      intended_end_user_role: this.metadataForm.value.educational_intended_end_user_role,
      context: this.metadataForm.value.educational_context,
      typical_age_range: this.metadataForm.value.educational_typical_age_range,
      difficulty: this.metadataForm.value.educational_difficulty,
      typical_learning_time: this.metadataForm.value.educational_stypical_learning_time,
      description: this.metadataForm.value.educational_description,
      language: this.metadataForm.value.educational_language,
    }
    let rights: RightsMetadata = {
      cost: this.metadataForm.value.rights_cost,
      copyright: this.metadataForm.value.rights_copyright,
      description: this.metadataForm.value.rights_description,
    }
    let relation: RelationMetadata = {
      kind: this.metadataForm.value.relation_kind,
      resource: this.metadataForm.value.relation_resource,
      annotation: this.metadataForm.value.relation_annotation,
    }
    let classification: ClassificationMetadata = {
      purpose: this.metadataForm.value.classification_purpose,
      taxon_path: this.metadataForm.value.classification_taxon_path,
      description: this.metadataForm.value.classification_description,
      keywords: this.metadataForm.value.classification_keywords,
    }
    let lifeCycle: LifeCycleMetadata = {
      version: this.metadataForm.value.lifeCycle_version,
      status: this.metadataForm.value.lifeCycle_status,
      contribute: this.metadataForm.value.lifeCycle_contribute,
    }
    let tehnical: TehnicalMetadata = {
      format: this.metadataForm.value.technical_format,
      size: this.metadataForm.value.technical_size,
      location: this.metadataForm.value.technical_location,
      requirement: this.metadataForm.value.technical_requirement,
      installation_remarks: this.metadataForm.value.technical_installation_remarks,
      duration: this.metadataForm.value.technical_duration,
    }
    let editMetadata: Metadata = {
      general: general,
      educational: educational,
      lifeCycle: lifeCycle,
      tehnical: tehnical,
      rights: rights,
      relation: relation,
      classification: classification
    }
    this.metadataService.editMetadata(editMetadata, this.selectedFileId).subscribe({
      next: () => {
        this.getMetadata(this.selectedFileId);
      },
      error: (err) => {
        console.log(err);
      }
    });
  }


  private getMetadata(id: number) {
    this.isLoading = true;
    this.metadataService.getFile(id).subscribe(
      res => {
        this.metadata = res;
        this.isLoading = false;

        this.metadataForm.patchValue({
          id: this.metadata.general.id,
          general_title: this.metadata.general.title,
          general_aggregation_level: this.metadata.general.aggregation_level,
          general_coverage: this.metadata.general.coverage,
          general_description: this.metadata.general.description,
          general_keywords: this.metadata.general.keywords,
          general_language: this.metadata.general.language,
          general_structure: this.metadata.general.structure,
          educational_context: this.metadata.educational.context,
          educational_description: this.metadata.educational.description,
          educational_difficulty: this.metadata.educational.difficulty,
          educational_intended_end_user_role: this.metadata.educational.intended_end_user_role,
          educational_interactivity_level: this.metadata.educational.interactivity_level,
          educational_interactivity_type: this.metadata.educational.interactivity_type,
          educational_language: this.metadata.educational.language,
          educational_learning_resource_type: this.metadata.educational.learning_resource_type,
          educational_semantic_density: this.metadata.educational.semantic_density,
          educational_stypical_learning_time: this.metadata.educational.typical_learning_time,
          educational_typical_age_range: this.metadata.educational.typical_age_range,
          lifeCycle_contribute: this.metadata.lifeCycle.contribute,
          lifeCycle_status: this.metadata.lifeCycle.status,
          lifeCycle_version: this.metadata.lifeCycle.version,
          classification_description: this.metadata.classification.description,
          classification_keywords: this.metadata.classification.keywords,
          classification_purpose: this.metadata.classification.purpose,
          classification_taxon_path: this.metadata.classification.taxon_path,
          rights_copyright: this.metadata.rights.copyright,
          rights_cost: this.metadata.rights.cost,
          rights_description: this.metadata.rights.description,
          relation_annotation: this.metadata.relation.annotation,
          relation_kind: this.metadata.relation.kind,
          relation_resource: this.metadata.relation.resource,
          technical_duration: this.metadata.tehnical.duration,
          technical_format: this.metadata.tehnical.format,
          technical_installation_remarks: this.metadata.tehnical.installation_remarks,
          technical_location: this.metadata.tehnical.location,
          technical_requirement: this.metadata.tehnical.requirement,
          technical_size: (this.metadata.tehnical.size)
        });
      }
    );
  }
}
