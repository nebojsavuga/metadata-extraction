export interface UploadedFile{
    id: number;
    name: string;
    size: number;
    user_id: number;
    file_path: string;
    folder_id: number;
}

export interface MetadataFolder{
    id: number,
    name: string,
    parent_folder_id: number
}