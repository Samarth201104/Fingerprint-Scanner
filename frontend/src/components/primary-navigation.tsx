"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [["Overview","/"],["Camera","/camera"],["Upload","/upload"],["Batch","/batch"],["Results","/results"]];

export default function PrimaryNavigation() {
  const pathname = usePathname();
  return <nav className="navLinks" aria-label="Main navigation">{links.map(([label, href]) => {
    const current = href === "/" ? pathname === "/" : pathname === href || pathname.startsWith(`${href}/`);
    return <Link href={href} key={href} aria-current={current ? "page" : undefined}>{label}</Link>;
  })}</nav>;
}
