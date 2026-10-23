"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { Camera, CameraOff, Check, Lightbulb, RefreshCw, ScanLine, Sun } from "lucide-react";
import { useRouter } from "next/navigation";
import { processImage, saveResult } from "@/services/api";

export default function CameraCapture() {
  const video = useRef<HTMLVideoElement>(null);
  const stream = useRef<MediaStream | null>(null);
  const [devices, setDevices] = useState<MediaDeviceInfo[]>([]);
  const [device, setDevice] = useState("");
  const [photo, setPhoto] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [starting, setStarting] = useState(true);
  const router = useRouter();

  async function start(id?: string) {
    setStarting(true); setError("");
    stream.current?.getTracks().forEach(track => track.stop());
    try {
      const next = await navigator.mediaDevices.getUserMedia({ audio: false, video: { deviceId: id ? { exact: id } : undefined, facingMode: id ? undefined : { ideal: "environment" }, width: { ideal: 1280 }, height: { ideal: 960 } } });
      stream.current = next;
      if (video.current) { video.current.srcObject = next; await video.current.play(); }
      const cameras = (await navigator.mediaDevices.enumerateDevices()).filter(item => item.kind === "videoinput");
      setDevices(cameras);
      setDevice(next.getVideoTracks()[0]?.getSettings().deviceId || cameras[0]?.deviceId || "");
    } catch (cause) {
      const denied = cause instanceof DOMException && (cause.name === "NotAllowedError" || cause.name === "SecurityError");
      setError(denied ? "Camera permission is blocked. Allow camera access in your browser settings, or upload an image instead." : "No camera is available right now. You can upload an image instead.");
    } finally { setStarting(false); }
  }

  useEffect(() => {
    void start();
    return () => stream.current?.getTracks().forEach(track => track.stop());
  }, []);

  function capture() {
    if (!video.current?.videoWidth || !video.current.videoHeight) { setError("The camera is still starting. Please wait a moment and try again."); return; }
    const canvas = document.createElement("canvas");
    canvas.width = video.current.videoWidth; canvas.height = video.current.videoHeight;
    const context = canvas.getContext("2d");
    if (!context) { setError("This browser could not capture the camera frame. Try uploading an image."); return; }
    context.drawImage(video.current, 0, 0);
    setPhoto(canvas.toDataURL("image/jpeg", .94)); setError("");
  }

  async function submit() {
    if (!photo) return;
    setBusy(true); setError("");
    try {
      const blob = await (await fetch(photo)).blob();
      const result = await processImage(new File([blob], "camera-capture.jpg", { type: "image/jpeg" }), "camera");
      saveResult(result); router.push(`/results/${result.job_id}`);
    } catch (cause) { setError(cause instanceof Error ? cause.message : "We couldn't process this image. Try again with a clearer capture."); }
    finally { setBusy(false); }
  }

  const status = error ? error : starting ? "Starting camera…" : photo ? "Capture ready to review" : device ? "Ready to capture · center your fingertip in the guide" : "Camera unavailable";
  return <div className="workspace">
    <section className="panel" aria-labelledby="camera-title">
      <div className="panelHeader"><h2 id="camera-title">Live camera</h2><p className="muted">Use a phone camera or webcam. A regular camera is not a certified fingerprint scanner.</p></div>
      <div className="cameraWrap">{photo ? <img src={photo} alt="Captured fingerprint image preview"/> : <video ref={video} playsInline muted aria-label="Live camera preview"/>}{!photo && device && <div className="guide" aria-hidden="true"/>}{!device && !starting && <div style={{position:"absolute",display:"grid",justifyItems:"center",gap:8,padding:20,textAlign:"center"}}><CameraOff size={28}/><span>Camera preview unavailable</span></div>}</div>
      <p className="cameraStatus" data-state={error ? "error" : "ready"} role={error ? "alert" : "status"} aria-live="polite"><i/>{status}</p>
      <div className="actions">{!photo ? <><button type="button" onClick={capture} disabled={!device || starting}><Camera size={16} aria-hidden="true"/>Capture image</button>{devices.length > 1 && <label className="smallNote">Camera<select className="select" aria-label="Select camera" value={device} onChange={event => { setDevice(event.target.value); void start(event.target.value); }}>{devices.map((item,index) => <option key={item.deviceId} value={item.deviceId}>{item.label || `Camera ${index+1}`}</option>)}</select></label>}</> : <><button type="button" onClick={submit} disabled={busy}><ScanLine size={16} aria-hidden="true"/>{busy ? "Processing image…" : "Process capture"}</button><button type="button" className="secondary" onClick={() => { setPhoto(""); setError(""); }} disabled={busy}><RefreshCw size={16} aria-hidden="true"/>Retake</button></>}</div>
      {busy && <p className="smallNote" role="status" aria-live="polite">Analyzing image and preparing the processing stages…</p>}
      {error && !device && <p className="actions"><Link className="button secondary" href="/upload">Upload an image instead</Link><button type="button" className="secondary" onClick={() => void start()}><RefreshCw size={15}/>Try camera again</button></p>}
    </section>
    <aside className="panel" aria-labelledby="guidance-title">
      <h2 id="guidance-title">Capture guidance</h2><p className="muted">The guide helps with framing; it does not measure image quality in real time.</p>
      <ul className="guidanceList"><li><Check size={16}/>Place the full fingertip inside the guide.</li><li><Sun size={16}/>Use bright, even light and avoid glare or shadows.</li><li><Lightbulb size={16}/>Hold still and move close enough to show ridge detail.</li><li><Check size={16}/>Keep the camera lens clean and avoid cropping the fingertip.</li></ul>
      <div className="infoBox">After capture, review the image before sending it to the processing pipeline.</div>
    </aside>
  </div>;
}
