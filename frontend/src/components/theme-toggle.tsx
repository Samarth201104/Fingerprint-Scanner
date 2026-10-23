"use client";

import { useEffect, useState } from "react";
import { Moon, Sun } from "lucide-react";

type Theme = "light" | "dark";

export default function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>("light");

  useEffect(() => {
    const saved = localStorage.getItem("fingerprint-theme") as Theme | null;
    const initial = saved || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    setTheme(initial);
    document.documentElement.dataset.theme = initial;
  }, []);

  function toggle() {
    const next = theme === "light" ? "dark" : "light";
    setTheme(next);
    document.documentElement.dataset.theme = next;
    localStorage.setItem("fingerprint-theme", next);
  }

  return <button className="themeControl" type="button" role="switch" aria-checked={theme === "dark"} onClick={toggle} aria-label={`Dark theme ${theme === "dark" ? "on" : "off"}`} title={`Switch to ${theme === "light" ? "dark" : "light"} theme`}>
    <span className="themeControlLabel"><Sun size={15} aria-hidden="true"/><span>Appearance</span></span>
    <span className="themeSwitch" aria-hidden="true"><span className="themeSwitchThumb">{theme === "light" ? <Sun size={12}/> : <Moon size={12}/>}</span></span>
  </button>;
}
