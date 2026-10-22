export interface ApiResponse<T> { success: boolean; message: string; data: T }
export interface ProcessingResult { job_id: string; status: string; filename: string; input_mode: string; images: Record<"original" | "roi" | "preprocessed" | "enhanced" | "binary" | "final", string>; metadata: { width: number; height: number; quality_score: number; processing_time_ms: number; warnings: string[] } }
export interface BatchResult { total: number; succeeded: number; failed: number; results: ({success:true;result:ProcessingResult}|{success:false;filename:string;error:string})[] }
