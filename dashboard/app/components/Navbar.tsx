"use client"; 
// Indique à Next.js que ce composant utilise du JavaScript côté client
// (obligatoire ici car on utilise useState et usePathname)

import Link from "next/link"; 
// Permet la navigation entre les pages sans recharger la page

import { usePathname } from "next/navigation"; 
// Permet de récupérer l’URL actuelle (pour savoir quel lien est actif)

import { useState } from "react"; 
// Hook React pour gérer l’état du menu mobile (ouvert / fermé)

export default function Navbar() {
  // Récupère le chemin actuel (/dashboard, /agents, etc.)
  const pathname = usePathname();

  // État pour ouvrir/fermer le menu mobile
  const [open, setOpen] = useState(false);

  /**
   * Fonction qui retourne la classe CSS d’un lien
   * - Bleu ciel si le lien est actif
   * - Bleu foncé sinon
   */
  const linkClass = (path: string) =>
    `block text-lg font-medium px-4 py-2 transition
     ${
       pathname === path
         ? "text-sky-500 underline underline-offset-8" // lien actif
         : "text-blue-700 hover:text-blue-500" // lien normal
     }`;

  return (
    // Barre de navigation principale
    <nav className="w-full bg-white shadow-sm">
      {/* Conteneur centré */}
      <div className="max-w-7xl mx-auto px-6">

        {/* Ligne supérieure de la navbar */}
        <div className="flex h-16 items-center justify-between">

          {/* Logo / Nom de l’application */}
          <div className="text-2xl font-bold text-blue-700">
            NetGuard Pro
          </div>

          {/* Menu Desktop (visible uniquement sur écran moyen et grand) */}
          <div className="hidden md:flex gap-10">
            <Link href="/" className={linkClass("/")}>
              Dashboard
            </Link>
            <Link href="/agents" className={linkClass("/agents")}>
              Agents
            </Link>
            <Link href="/alerts" className={linkClass("/alerts")}>
              Alerts
            </Link>
            <Link href="/stats" className={linkClass("/stats")}>
              Statistics
            </Link>
          </div>

          {/* Bouton menu mobile (visible uniquement sur petit écran) */}
          <button
            onClick={() => setOpen(!open)} // ouvre ou ferme le menu
            className="md:hidden text-blue-700 text-3xl"
          >
            ☰
          </button>
        </div>

        {/* Menu Mobile (affiché seulement si open === true) */}
        {open && (
          <div className="md:hidden flex flex-col gap-2 pb-4">

            {/* Chaque clic ferme automatiquement le menu */}
            <Link
              href="/"
              className={linkClass("/")}
              onClick={() => setOpen(false)}
            >
              Dashboard
            </Link>

            <Link
              href="/agents"
              className={linkClass("/agents")}
              onClick={() => setOpen(false)}
            >
              Agents
            </Link>

            <Link
              href="/alerts"
              className={linkClass("/alerts")}
              onClick={() => setOpen(false)}
            >
              Alerts
            </Link>

            <Link
              href="/stats"
              className={linkClass("/stats")}
              onClick={() => setOpen(false)}
            >
              Statistics
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}
