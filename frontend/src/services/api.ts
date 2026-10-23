import type { ApiResponse, ProcessingResult, BatchResult } from "@/types/api";
const API = (process.env.NEXT_PUBLIC_API_URL || (process.env.NODE_ENV === "development" ? "http://localhost:8000" : "")).replace(/\/+$/, "");
function apiUrl(path: string) {
  if (!API) throw new Error("Set NEXT_PUBLIC_API_URL to the deployed backend URL.");
  return `${API}${path}`;
}
export function resolveImageUrl(path: string) { return /^https?:\/\//i.test(path) ? path : apiUrl(path); }
export function saveResult(result: ProcessingResult) {
  sessionStorage.setItem("fingerprint-result", JSON.stringify(result));
  const previous = JSON.parse(sessionStorage.getItem("fingerprint-history") || "[]") as ProcessingResult[];
  sessionStorage.setItem("fingerprint-history", JSON.stringify([result, ...previous.filter(item => item.job_id !== result.job_id)].slice(0, 30)));
}
async function request<T>(path: string, body: FormData): Promise<ApiResponse<T>> {
  let response: Response;
  try { response = await fetch(apiUrl(path), { method: "POST", body }); }
  catch { throw new Error("Unable to connect to the processing server."); }
  const json = await response.json();
  if (!response.ok) throw new Error(json.detail?.message || json.message || "Fingerprint processing failed.");
  return json;
}
export async function processImage(file: File, mode = "upload") { const form = new FormData(); form.append("file", file); form.append("input_mode", mode); return (await request<ProcessingResult>("/api/v1/fingerprint/process", form)).data; }
export async function processBatch(files: File[]) { const form = new FormData(); files.forEach(file => form.append("files", file)); return (await request<BatchResult>("/api/v1/fingerprint/process-batch", form)).data; }
export async function checkHealth() { if (!API) return false; try { return (await fetch(apiUrl("/api/v1/health"))).ok; } catch { return false; } }
