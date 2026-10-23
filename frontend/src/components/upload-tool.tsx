"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Check, ImagePlus, ScanLine, Sun, X } from "lucide-react";
import { processImage, saveResult } from "@/services/api";

const MAX_FILE_SIZE = 12 * 1024 * 1024;
const ACCEPTED_TYPES = /^image\/(jpeg|png|bmp|webp)$/;

export default function UploadTool({ mode = "upload" }: { mode?: string }) {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  useEffect(() => {
    if (!file) { setPreview(null); return; }
    const url = URL.createObjectURL(file);
    setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  function choose(next?: File) {
    if (!next) return;
    setError("");
    if (!ACCEPTED_TYPES.test(next.type) || next.size > MAX_FILE_SIZE) {
      setError("Choose a JPG, PNG, BMP, or WEBP image under 12 MB.");
      return;
    }
    setFile(next);
  }

  async function submit() {
    if (!file) return;
    setBusy(true); setError("");
    try {
      const result = await processImage(file, mode);
      saveResult(result);
      router.push(`/results/${result.job_id}`);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "We couldn't process this image. Try again with a clearer capture.");
    } finally { setBusy(false); }
  }

  return <div className="workspace">
    <section className="panel" aria-labelledby="upload-panel-title">
      <div className="panelHeader"><h2 id="upload-panel-title">Image input</h2><p className="muted">JPG, PNG, BMP, or WEBP · up to 12 MB</p></div>
      {!file ? <div className="drop" onDragOver={event => event.preventDefault()} onDrop={event => { event.preventDefault(); choose(event.dataTransfer.files[0]); }}>
        <ImagePlus size={26} aria-hidden="true" color="var(--accent-strong)"/><p><strong>Drop a fingerprint image here</strong></p><label className="button secondary">Browse files<input className="visuallyHidden" type="file" accept="image/jpeg,image/png,image/bmp,image/webp" aria-label="Choose fingerprint image" onChange={event => choose(event.target.files?.[0])}/></label>
      </div> : <>
        {preview && <img className="preview" src={preview} alt={`Selected fingerprint preview: ${file.name}`}/>}
        <p className="smallNote" style={{marginBottom:0,marginTop:10}}>{file.name} · {(file.size / 1024 / 1024).toFixed(2)} MB</p>
        <div className="actions"><button type="button" onClick={submit} disabled={busy}><ScanLine size={16} aria-hidden="true"/>{busy ? "Processing image…" : "Process fingerprint"}</button><button type="button" className="secondary" onClick={() => { setFile(null); setError(""); }} disabled={busy}><X size={16} aria-hidden="true"/>Remove image</button></div>
        {busy && <p className="cameraStatus" role="status" aria-live="polite"><i/>Analyzing image and preparing the processing stages…</p>}
      </>}
      {error && <div className="error" role="alert">{error}</div>}
    </section>
    <aside className="panel" aria-labelledby="quality-title">
      <h2 id="quality-title">Capture for clear ridges</h2>
      <p className="muted">Sharp, evenly lit images help the pipeline preserve visible fingerprint detail.</p>
      <ul className="guidanceList"><li><Sun size={16}/>Use bright, even lighting; avoid glare and deep shadows.</li><li><Check size={16}/>Keep the full fingertip visible and centered.</li><li><Check size={16}/>Hold steady to reduce motion blur.</li></ul>
      <div className="infoBox">The system returns quality metadata and the original, ROI, normalized, enhanced, binary, and final images.</div>
    </aside>
  </div>;
}
