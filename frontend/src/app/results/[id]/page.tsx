"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, Download } from "lucide-react";
import type { ProcessingResult } from "@/types/api";
import { resolveImageUrl } from "@/services/api";

const stages = [
  ["original", "Original", "Uploaded or captured image"],
  ["roi", "Fingerprint region", "Extracted region of interest"],
  ["preprocessed", "Normalized", "Grayscale and contrast normalized"],
  ["enhanced", "Enhanced", "Gabor ridge enhancement"],
  ["binary", "Binary", "Adaptive threshold output"],
  ["final", "Final output", "Morphological post-processing"],
] as const;

export default function ResultDetail() {
  const params = useParams<{ id: string }>();
  const [result, setResult] = useState<ProcessingResult | null>(null);
  useEffect(() => {
    try {
      const history = JSON.parse(sessionStorage.getItem("fingerprint-history") || "[]") as ProcessingResult[];
      setResult(history.find(item => item.job_id === params.id) || null);
    } catch { setResult(null); }
  }, [params.id]);

  if (!result) return <section className="panel emptyState"><h1>Result unavailable</h1><p className="muted">This result is not saved in this browser session, or its temporary image files may have expired.</p><Link className="button" href="/upload">Process another image</Link></section>;

  return <>
    <div className="pageTitle"><Link href="/results" className="textLink"><ArrowLeft size={15}/>All results</Link><p className="eyebrow" style={{marginTop:18}}>Processing complete · {result.job_id.slice(0,10)}</p><h1>{result.filename}</h1>
      <div className="meta"><span className="metaItem">Quality score {result.metadata.quality_score}/100</span><span className="metaItem">{result.metadata.processing_time_ms} ms</span><span className="metaItem">{result.metadata.width} × {result.metadata.height} px</span><span className="metaItem">Input: {result.input_mode}</span></div>
      {result.metadata.warnings.map(warning => <div className="infoBox" key={warning} role="note">{warning}</div>)}
    </div>
    <section aria-labelledby="stages-title"><div className="sectionHead"><div><span className="eyebrow">Image comparison</span><h2 id="stages-title">Processing stages</h2></div></div>
      <div className="resultGrid">{stages.map(([key,title,description],index) => { const src = resolveImageUrl(result.images[key]); return <article className="resultTile" key={key}><a href={src} target="_blank" rel="noreferrer" aria-label={`Open ${title} image in a new tab`}><img src={src} alt={`${title} fingerprint processing stage`} loading={index < 2 ? "eager" : "lazy"}/></a><div className="resultTileTitle"><span>{title}</span><small>{String(index+1).padStart(2,"0")}</small></div><p className="smallNote">{description}</p>{key !== "original" && <a download={`${result.filename}-${key}.png`} href={resolveImageUrl(result.images[key].replace("/image/","/download/"))} className="arrow"><Download size={14}/>Download image</a>}</article>; })}</div>
    </section>
    <div className="actions"><Link className="button secondary" href="/upload">Process another image</Link><Link className="button secondary" href="/results">View session history</Link></div>
  </>;
}
