import Link from "next/link";
import { Aperture, ArrowUpRight, Camera, Files, Fingerprint, Image as ImageIcon, ShieldAlert } from "lucide-react";

const actions = [
  { title: "Capture with camera", description: "Use a phone or webcam to acquire a fingerprint image.", href: "/camera", icon: Camera, action: "Open camera" },
  { title: "Upload an image", description: "Process one supported image and review each returned stage.", href: "/upload", icon: ImageIcon, action: "Choose image" },
  { title: "Batch processing", description: "Process up to 50 images independently and download a ZIP.", href: "/batch", icon: Files, action: "Open batch tool" },
];

const pipeline = [
  ["01", "Acquire image", "Capture from a camera or upload a fingerprint image."],
  ["02", "Inspect quality", "Estimate sharpness, contrast, brightness, and image dimensions."],
  ["03", "Extract ROI", "Select the fingerprint region of interest for processing."],
  ["04", "Normalize contrast", "Apply grayscale conversion, blur, and CLAHE normalization."],
  ["05", "Enhance ridges", "Use Gabor filtering to enhance fingerprint ridge patterns."],
  ["06", "Threshold & clean", "Create a binary image, then apply morphological post-processing."],
];

export default function Home() {
  return <>
    <section className="hero" aria-labelledby="home-title">
      <div>
        <span className="eyebrow">Computer vision workspace</span>
        <h1 id="home-title">Fingerprint image acquisition &amp; enhancement</h1>
        <p className="lead">Capture or upload a fingerprint image, run it through a shared OpenCV pipeline, and inspect the original alongside its processing stages.</p>
        <div className="capabilities"><span className="pill">OpenCV pipeline</span><span className="pill">Camera + upload</span><span className="pill">Single + batch</span></div>
      </div>
      <div className="heroArt" aria-hidden="true"><Fingerprint size={96} strokeWidth={1.1}/><span className="heroCaption">IMAGE LAB / 01</span></div>
    </section>

    <section aria-labelledby="start-title">
      <div className="sectionHead"><div><span className="eyebrow">Image acquisition</span><h2 id="start-title">Start a scan</h2></div><Link className="textLink" href="/results">View recent results <ArrowUpRight size={15}/></Link></div>
      <div className="grid">{actions.map(({ title, description, href, icon: Icon, action }) => <Link href={href} className="card" key={href}><div className="cardIcon"><Icon size={21}/></div><h3>{title}</h3><p>{description}</p><span className="arrow">{action}<ArrowUpRight size={14}/></span></Link>)}</div>
    </section>

    <section className="section" aria-labelledby="pipeline-title">
      <div className="sectionHead"><div><span className="eyebrow">From input to output</span><h2 id="pipeline-title">Computer vision pipeline</h2></div></div>
      <div className="pipeline">{pipeline.map(([number,title,description]) => <article className="pipelineStep" key={number}><span className="stepNumber">{number}</span><strong>{title}</strong><p>{description}</p></article>)}</div>
      <div className="notePanel"><div className="cardIcon"><Aperture size={20}/></div><div><h3>Better input helps preserve ridge detail</h3><p className="muted" style={{marginBottom:0}}>Use bright, even lighting. Avoid glare, deep shadows, motion blur, and partially visible fingertips.</p></div></div>
    </section>
    <div className="infoBox" style={{display:"flex",gap:10,alignItems:"flex-start"}}><ShieldAlert size={18} aria-hidden="true"/><span>This tool enhances fingerprint images for inspection. It is not a certified biometric authentication system.</span></div>
  </>;
}
