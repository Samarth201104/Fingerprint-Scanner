import type { Metadata } from "next";
import Link from "next/link";
import { Fingerprint } from "lucide-react";
import ThemeToggle from "@/components/theme-toggle";
import PrimaryNavigation from "@/components/primary-navigation";
import "./globals.css";
export const metadata: Metadata = { title: "Fingerprint Scanner AI", description: "Camera-based fingerprint image acquisition and enhancement system." };
export default function RootLayout({children}:{children:React.ReactNode}) { return <html lang="en"><body><header className="topbar"><Link className="brand" href="/"><span className="brandIcon"><Fingerprint size={22}/></span><span>Fingerprint <b>Scanner AI</b><small>COMPUTER VISION WORKSPACE</small></span></Link><PrimaryNavigation/><div className="headerActions"><span className="workspaceLabel">Image acquisition lab</span><ThemeToggle/></div></header><main id="main-content">{children}</main><footer><span>Fingerprint Scanner AI</span><span>Camera-based fingerprint image acquisition and enhancement system</span></footer></body></html> }
