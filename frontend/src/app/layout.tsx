import type { Metadata } from "next";
import Link from "next/link";
import { Activity, Fingerprint } from "lucide-react";
import "./globals.css";
export const metadata: Metadata = { title: "Fingerprint Scanner AI", description: "Camera-based fingerprint image acquisition and enhancement system." };
const links = [["Overview","/"],["Camera","/camera"],["Upload","/upload"],["Batch","/batch"],["Results","/results"]];
export default function RootLayout({children}:{children:React.ReactNode}) { return <html lang="en"><body><header className="topbar"><Link className="brand" href="/"><span className="brandIcon"><Fingerprint size={24}/></span><span>Fingerprint <b>Scanner AI</b><small>IMAGE LAB</small></span></Link><nav>{links.map(([label,href])=><Link href={href} key={href}>{label}</Link>)}</nav><span className="apiStatus"><i/> CV pipeline ready</span></header><main>{children}</main><footer><span>Fingerprint Scanner AI</span><span>Camera-based fingerprint image acquisition and enhancement system</span></footer></body></html> }
