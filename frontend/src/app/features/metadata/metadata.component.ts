import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import {
  ClassificationMetadata, EducationalMetadata, GeneralMetadata, LifeCycleMetadata, Metadata,
  RightsMetadata, TehnicalMetadata
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
  showGeneral = false;
  showEducational = false;
  showLifecycle = false;
  showClassification = false;
  showRights = false;
  showTechnical = false;

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
      title: this.metadataForm.value.general_title?.toLocaleLowerCase(),
      description: this.metadataForm.value.general_description?.toLocaleLowerCase(),
      language: this.metadataForm.value.general_language?.toLocaleLowerCase(),
      keywords: this.metadataForm.value.general_keywords?.toLocaleLowerCase(),
      structure: this.metadataForm.value.general_structure?.toLocaleLowerCase(),
      coverage: this.metadataForm.value.general_coverage?.toLocaleLowerCase(),
      aggregation_level: this.metadataForm.value.general_aggregation_level?.toLocaleLowerCase()
    };
    let educational: EducationalMetadata = {
      interactivity_type: this.metadataForm.value.educational_interactivity_type?.toLocaleLowerCase(),
      learning_resource_type: this.metadataForm.value.educational_learning_resource_type?.toLocaleLowerCase(),
      interactivity_level: this.metadataForm.value.educational_interactivity_level?.toLocaleLowerCase(),
      semantic_density: this.metadataForm.value.educational_semantic_density?.toLocaleLowerCase(),
      intended_end_user_role: this.metadataForm.value.educational_intended_end_user_role?.toLocaleLowerCase(),
      context: this.metadataForm.value.educational_context?.toLocaleLowerCase(),
      typical_age_range: this.metadataForm.value.educational_typical_age_range?.toLocaleLowerCase(),
      difficulty: this.metadataForm.value.educational_difficulty?.toLocaleLowerCase(),
      typical_learning_time: this.metadataForm.value.educational_stypical_learning_time?.toLocaleLowerCase(),
      description: this.metadataForm.value.educational_description?.toLocaleLowerCase()
    };

    let rights: RightsMetadata = {
      cost: this.metadataForm.value.rights_cost?.toLocaleLowerCase(),
      copyright: this.metadataForm.value.rights_copyright?.toLocaleLowerCase(),
      description: this.metadataForm.value.rights_description?.toLocaleLowerCase()
    };

    let classification: ClassificationMetadata = {
      purpose: this.metadataForm.value.classification_purpose?.toLocaleLowerCase(),
      taxon_path: this.metadataForm.value.classification_taxon_path?.toLocaleLowerCase(),
      description: this.metadataForm.value.classification_description?.toLocaleLowerCase(),
      keywords: this.metadataForm.value.classification_keywords?.toLocaleLowerCase()
    };

    let lifeCycle: LifeCycleMetadata = {
      version: this.metadataForm.value.lifeCycle_version?.toLocaleLowerCase(),
      status: this.metadataForm.value.lifeCycle_status?.toLocaleLowerCase(),
      contribute: this.metadataForm.value.lifeCycle_contribute?.toLocaleLowerCase()
    };

    let tehnical: TehnicalMetadata = {
      format: this.metadataForm.value.technical_format?.toLocaleLowerCase(),
      size: this.metadataForm.value.technical_size?.toLocaleLowerCase(),
      location: this.metadataForm.value.technical_location?.toLocaleLowerCase(),
      requirement: this.metadataForm.value.technical_requirement?.toLocaleLowerCase(),
      installation_remarks: this.metadataForm.value.technical_installation_remarks?.toLocaleLowerCase(),
      duration: this.metadataForm.value.technical_duration?.toLocaleLowerCase()
    };
    let editMetadata: Metadata = {
      general: general,
      educational: educational,
      lifeCycle: lifeCycle,
      tehnical: tehnical,
      rights: rights,
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
          general_title: this.metadata.general.title?.toLocaleLowerCase(),
          general_aggregation_level: this.metadata.general.aggregation_level?.toLocaleLowerCase(),
          general_coverage: this.metadata.general.coverage?.toLocaleLowerCase(),
          general_description: this.metadata.general.description?.toLocaleLowerCase(),
          general_keywords: this.metadata.general.keywords?.toLocaleLowerCase(),
          general_language: this.metadata.general.language?.toLocaleLowerCase(),
          general_structure: this.metadata.general.structure?.toLocaleLowerCase(),
          educational_context: this.metadata.educational.context?.toLocaleLowerCase(),
          educational_description: this.metadata.educational.description?.toLocaleLowerCase(),
          educational_difficulty: this.metadata.educational.difficulty?.toLocaleLowerCase(),
          educational_intended_end_user_role: this.metadata.educational.intended_end_user_role?.toLocaleLowerCase(),
          educational_interactivity_level: this.metadata.educational.interactivity_level?.toLocaleLowerCase(),
          educational_interactivity_type: this.metadata.educational.interactivity_type?.toLocaleLowerCase(),
          educational_learning_resource_type: this.metadata.educational.learning_resource_type?.toLocaleLowerCase(),
          educational_semantic_density: this.metadata.educational.semantic_density?.toLocaleLowerCase(),
          educational_stypical_learning_time: this.metadata.educational.typical_learning_time?.toLocaleLowerCase(),
          educational_typical_age_range: this.metadata.educational.typical_age_range?.toLocaleLowerCase(),
          lifeCycle_contribute: this.metadata.lifeCycle.contribute?.toLocaleLowerCase(),
          lifeCycle_status: this.metadata.lifeCycle.status?.toLocaleLowerCase(),
          lifeCycle_version: this.metadata.lifeCycle.version?.toLocaleLowerCase(),
          classification_description: this.metadata.classification.description?.toLocaleLowerCase(),
          classification_keywords: this.metadata.classification.keywords?.toLocaleLowerCase(),
          classification_purpose: this.metadata.classification.purpose?.toLocaleLowerCase(),
          classification_taxon_path: this.metadata.classification.taxon_path?.toLocaleLowerCase(),
          rights_copyright: this.metadata.rights.copyright?.toLocaleLowerCase(),
          rights_cost: this.metadata.rights.cost?.toLocaleLowerCase(),
          rights_description: this.metadata.rights.description?.toLocaleLowerCase(),
          technical_duration: this.metadata.tehnical.duration?.toLocaleLowerCase(),
          technical_format: this.metadata.tehnical.format?.toLocaleLowerCase(),
          technical_installation_remarks: this.metadata.tehnical.installation_remarks?.toLocaleLowerCase(),
          technical_location: this.metadata.tehnical.location?.toLocaleLowerCase(),
          technical_requirement: this.metadata.tehnical.requirement?.toLocaleLowerCase(),
          technical_size: this.metadata.tehnical.size?.toLocaleLowerCase()
        });
      }
    );
  }

  changeShowGeneral() {
    this.showGeneral = !this.showGeneral;
  }

  changeShowEducational() {
    this.showEducational = !this.showEducational;
  }

  changeShowLifecycle() {
    this.showLifecycle = !this.showLifecycle;
  }

  changeShowClassification() {
    this.showClassification = !this.showClassification;
  }

  changeShowRights() {
    this.showRights = !this.showRights;
  }

  changeShowTechnical() {
    this.showTechnical = !this.showTechnical;
  }
}
