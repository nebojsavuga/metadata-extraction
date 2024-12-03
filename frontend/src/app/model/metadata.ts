export interface Metadata {
    general: GeneralMetadata;
    lifeCycle: LifeCycleMetadata;
    tehnical: TehnicalMetadata;
    educational: EducationalMetadata;
    rights: RightsMetadata;
    relation: RelationMetadata;
    classification: ClassificationMetadata;
}

export interface GeneralMetadata {
    id: string;
    title: string;
    language: string;
    description: string;
    keywords: string;
    structure: string;
    coverage: string;
    aggregation_level: string;
}

export interface LifeCycleMetadata {
    version: string;
    status: string;
    contribute: string;
}

export interface TehnicalMetadata {
    format: string;
    size: string;
    location: string;
    requirement: string;
    installation_remarks: string;
    duration: string;
}

export interface EducationalMetadata {
    interactivity_type: string;
    learning_resource_type: string;
    interactivity_level: string;
    semantic_density: string;
    intended_end_user_role: string;
    context: string;
    typical_age_range: string;
    difficulty: string;
    typical_learning_time: string;
    description: string;
    language: string;
}

export interface RightsMetadata {
    cost: string;
    copyright: string;
    description: string;
}

export interface RelationMetadata {
    kind: string;
    resource: string;
    annotation: string;
}

export interface ClassificationMetadata {
    purpose: string;
    taxon_path: string;
    description: string;
    keywords: string;
}
