import type { ApiResponse, ProcessingResult, BatchResult } from "@/types/api";
const API = (process.env.NEXT_PUBLIC_API_URL || "").replace(/\/+$/, "");
function apiUrl(path: string) {
  if (!API) throw new Error("Image processing isn't configured yet. Please contact the site administrator.");
  return `${API}${path}`;
}
export function resolveImageUrl(path: string) { return /^https?:\/\//i.test(path) ? path : apiUrl(path); }
export function saveResult(result: ProcessingResult) {
  sessionStorage.setItem("fingerprint-result", JSON.stringify(result));
  const previous = JSON.parse(sessionStorage.getItem("fingerprint-history") || "[]") as ProcessingResult[];
  sessionStorage.setItem("fingerprint-history", JSON.stringify([result, ...previous.filter(item => item.job_id !== result.job_id)].slice(0, 30)));
}
async function request<T>(path: string, body: FormData): Promise<ApiResponse<T>> {
  // Resolve configuration before fetch so a missing production URL is not
  // incorrectly reported as a network/CORS failure.
  const url = apiUrl(path);
  let response: Response;
  try { response = await fetch(url, { method: "POST", body }); }
  catch {
    throw new Error("Unable to reach the image processing service. Check your connection and try again.");
  }
  let json: ApiResponse<T> & { detail?: { message?: string }; message?: string };
  try { json = await response.json(); }
  catch { throw new Error("The processing service returned an unreadable response. Please try again."); }
  if (!response.ok) throw new Error(json.detail?.message || json.message || "We couldn't process this image. Try a clearer capture.");
  return json;
}
export async function processImage(file: File, mode = "upload") { const form = new FormData(); form.append("file", file); form.append("input_mode", mode); return (await request<ProcessingResult>("/api/v1/fingerprint/process", form)).data; }
export async function processBatch(files: File[]) { const form = new FormData(); files.forEach(file => form.append("files", file)); return (await request<BatchResult>("/api/v1/fingerprint/process-batch", form)).data; }
export async function checkHealth() { if (!API) return false; try { return (await fetch(apiUrl("/api/v1/health"))).ok; } catch { return false; } }
